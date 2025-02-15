import copy
import awkward as ak
from coffea import processor
from coffea.analysis_tools import PackedSelection, Weights
from analysis.configs import ProcessorConfigBuilder
from analysis.histograms import HistBuilder, fill_histogram
from analysis.selections import (
    ObjectSelector,
    get_lumi_mask,
    get_trigger_mask,
    get_trigger_match_mask,
    get_metfilters_mask,
    get_stitching_mask,
    get_hemcleaning_mask,
)
from analysis.corrections import (
    TauCorrector,
    BTagCorrector,
    MuonCorrector,
    ElectronCorrector,
    MuonHighPtCorrector,
    add_pileup_weight,
    add_pujetid_weight,
    update_met_jet_veto,
    apply_jet_corrections,
    add_l1prefiring_weight,
    apply_met_phi_corrections,
    apply_rochester_corrections,
    apply_tau_energy_scale_corrections,
)


def update(events, collections):
    """Return a shallow copy of events array with some collections swapped out"""
    out = events
    for name, value in collections.items():
        out = ak.with_field(out, value, name)
    return out


class ZToJets(processor.ProcessorABC):
    def __init__(
        self,
        year: str = "2017",
        flow: str = "True",
        do_systematics: bool = False
    ):
        self.year = year
        self.flow = flow
        self.do_systematics = do_systematics

        config_builder = ProcessorConfigBuilder(processor="ztojets", year=year)
        self.processor_config = config_builder.build_processor_config()
        self.histogram_config = self.processor_config.histogram_config
        self.histograms = HistBuilder(self.processor_config).build_histogram()
        
    def process(self, events):
        # check if sample is MC
        self.is_mc = hasattr(events, "genWeight")
        if not self.is_mc:
            # nominal JEC are already applied in data
            return self.process_shift(events, shift_name="nominal")

        # apply JEC/JER corrections to jets (in data, the corrections are already applied)
        apply_jet_corrections(events, self.year)
        # define Jet/MET shifts
        shifts = [({"Jet": events.Jet, "MET": events.MET}, "nominal")]
        if self.do_systematics:
            shifts.extend([
                ({"Jet": events.Jet.JES_jes.up, "MET": events.MET.JES_jes.up},"JESUp"),
                ({"Jet": events.Jet.JES_jes.down, "MET": events.MET.JES_jes.down},"JESDown"),
                ({"Jet": events.Jet.JER.up, "MET": events.MET.JER.up}, "JERUp"),
                ({"Jet": events.Jet.JER.down, "MET": events.MET.JER.down},"JERDown"),
                ({"Jet": events.Jet, "MET": events.MET.MET_UnclusteredEnergy.up}, "UESUp"),
                ({"Jet": events.Jet,"MET": events.MET.MET_UnclusteredEnergy.down,},"UESDown"),
            ])
        return processor.accumulate(
            self.process_shift(update(events, collections), name)
            for collections, name in shifts
        )
                
    def process_shift(self, events, shift_name):
        year = self.year
        is_mc = self.is_mc
        # get number of events
        nevents = len(events)
        # get dataset name
        dataset = events.metadata["dataset"]
        # get golden json, HLT paths and selections
        goldenjson = self.processor_config.goldenjson
        hlt_paths = self.processor_config.hlt_paths
        object_selection = self.processor_config.object_selection
        event_selection = self.processor_config.event_selection
        # create copies of histogram objects
        hist_dict = copy.deepcopy(self.histograms)
        # initialize output dictionary
        output = {}
        output["metadata"] = {}
        if shift_name == "nominal":
            output["metadata"].update({"raw_initial_nevents": nevents})

        # -------------------------------------------------------------
        # object corrections
        # -------------------------------------------------------------
        if is_mc:
            # apply energy corrections to taus (only to MC)
            apply_tau_energy_scale_corrections(
                events=events, year=year, variation=shift_name
            )
        # apply rochester corretions to muons
        apply_rochester_corrections(
            events=events, is_mc=is_mc, year=year, variation=shift_name
        )
        # apply MET phi modulation corrections
        apply_met_phi_corrections(
            events=events,
            is_mc=is_mc,
            year=year,
        )
        # propagate jet_veto maps to MET
        if "jetsvetomaps" in object_selection["jets"]["cuts"]:
            update_met_jet_veto(events, year)

        # -------------------------------------------------------------
        # event SF/weights computation
        # -------------------------------------------------------------
        # set weights container
        weights_container = Weights(len(events), storeIndividual=True)
        if is_mc:
            # add gen weigths
            weights_container.add("genweight", events.genWeight)
            # add l1prefiring weigths
            add_l1prefiring_weight(events, weights_container, year, shift_name)
            # add pileup weigths
            add_pileup_weight(events, weights_container, year, shift_name)
            # add pujetid weigths
            add_pujetid_weight(
                jets=events.Jet,
                weights=weights_container,
                year=year,
                working_point=object_selection["jets"]["cuts"]["jets_pileup_id"],
                variation=shift_name,
            )
            # b-tagging corrector
            btag_corrector = BTagCorrector(
                events=events,
                weights=weights_container,
                sf_type="comb",
                worging_point=object_selection["bjets"]["cuts"]["jets_deepjet_b"],
                year=year,
                full_run=False,
                variation=shift_name,
            )
            # add b-tagging weights
            btag_corrector.add_btag_weights(flavor="bc")
            btag_corrector.add_btag_weights(flavor="light")
            # electron corrector
            electron_corrector = ElectronCorrector(
                electrons=events.Electron,
                weights=weights_container,
                year=year,
            )
            # add electron ID weights
            electron_corrector.add_id_weight(
                id_working_point=object_selection["electrons"]["cuts"][
                    "electrons_id"
                ],
            )
            # add electron reco weights
            electron_corrector.add_reco_weight("RecoAbove20")
            electron_corrector.add_reco_weight("RecoBelow20")

            # muon corrector
            muon_corrector_args = {
                "events": events,
                "weights": weights_container,
                "year": year,
                "variation": shift_name,
                "id_wp": object_selection["muons"]["cuts"]["muons_id"],
                "iso_wp": object_selection["muons"]["cuts"]["muons_iso"],
            }
            muon_corrector = (
                MuonHighPtCorrector(**muon_corrector_args)
                if object_selection["muons"]["cuts"]["muons_id"] == "highpt"
                else MuonCorrector(**muon_corrector_args)
            )
            # add muon RECO weights
            muon_corrector.add_reco_weight()
            # add muon ID weights
            muon_corrector.add_id_weight()
            # add muon iso weights
            muon_corrector.add_iso_weight()
            # add trigger weights
            muon_corrector.add_triggeriso_weight(hlt_paths)

            # add tau weights
            tau_corrector = TauCorrector(
                events=events,
                weights=weights_container,
                year=year,
                tau_vs_jet=object_selection["taus"]["cuts"]["taus_vs_jet"],
                tau_vs_ele=object_selection["taus"]["cuts"]["taus_vs_ele"],
                tau_vs_mu=object_selection["taus"]["cuts"]["taus_vs_mu"],
                variation=shift_name,
            )
            tau_corrector.add_id_weight_deeptauvse()
            tau_corrector.add_id_weight_deeptauvsmu()
            tau_corrector.add_id_weight_deeptauvsjet()
                
        if shift_name == "nominal":
            # save sum of weights before object_selection
            output["metadata"].update({"sumw": ak.sum(weights_container.weight())})
                
        # -------------------------------------------------------------
        # object selection
        # -------------------------------------------------------------
        object_selector = ObjectSelector(object_selection, year)
        objects = object_selector.select_objects(events)
        # -------------------------------------------------------------
        # event selection
        # -------------------------------------------------------------
        # itinialize selection manager
        selection_manager = PackedSelection()
        # add all selections to selector manager
        for selection, mask in event_selection["selections"].items():
            selection_manager.add(selection, eval(mask))

        categories = event_selection["categories"]
        for category, category_cuts in categories.items():
            # get selection mask by category
            category_mask = selection_manager.all(*category_cuts)
            nevents_after = ak.sum(category_mask)

            if shift_name == "nominal":
                # save cutflow to metadata
                output["metadata"][category] = {"cutflow": {}}
                selections = []
                for cut_name in category_cuts:
                    selections.append(cut_name)
                    current_selection = selection_manager.all(*selections)
                    output["metadata"][category]["cutflow"][cut_name] = ak.sum(
                        weights_container.weight()[current_selection]
                    )
                # save number of events after selection to metadata
                output["metadata"][category].update(
                    {
                        "weighted_final_nevents": ak.sum(
                            weights_container.weight()[category_mask]
                        ),
                        "raw_final_nevents": nevents_after,
                    }
                )
            # -------------------------------------------------------------
            # analysis variables
            # -------------------------------------------------------------
            # check that there are events left after selection
            if nevents_after > 0:
                # build analysis variables map
                variables_map = {}
                for variable, axis in self.histogram_config.axes.items():
                    variables_map[variable] = eval(axis.expression)[category_mask]
                # -------------------------------------------------------------
                # histogram filling
                # -------------------------------------------------------------
                # break up the histogram filling for event-wise variations and object-wise variations
                # apply event-wise variations only for nominal
                if is_mc and shift_name == "nominal":
                    # get event weight systematic variations for MC samples
                    variations = ["nominal"] + list(weights_container.variations)
                    for variation in variations:
                        if variation == "nominal":
                            category_weight = weights_container.weight()[
                                category_mask
                            ]
                        else:
                            category_weight = weights_container.weight(
                                modifier=variation
                            )[category_mask]
                        fill_histogram(
                            histograms=hist_dict,
                            histogram_config=self.histogram_config,
                            variables_map=variables_map,
                            weights=category_weight,
                            variation=variation,
                            category=category,
                            flow=self.flow,
                        )
                else:
                    # fill Data/object-wise variations for MC samples
                    category_weight = weights_container.weight()[category_mask]
                    fill_histogram(
                        histograms=hist_dict,
                        histogram_config=self.histogram_config,
                        variables_map=variables_map,
                        weights=category_weight,
                        variation=shift_name,
                        category=category,
                        flow=self.flow,
                    )
        # define output dictionary accumulator
        output["histograms"] = hist_dict
        return output

    def postprocess(self, accumulator):
        return accumulator