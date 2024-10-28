import copy
import awkward as ak
from coffea import processor
from coffea.analysis_tools import PackedSelection, Weights
from analysis.configs import ProcessorConfigBuilder
from analysis.histograms import HistBuilder, fill_histogram
from analysis.corrections.jec import apply_jet_corrections
from analysis.corrections.met import apply_met_phi_corrections
from analysis.corrections.rochester import apply_rochester_corrections
from analysis.corrections.tau_energy import apply_tau_energy_scale_corrections
from analysis.corrections.pileup import add_pileup_weight
from analysis.corrections.l1prefiring import add_l1prefiring_weight
from analysis.corrections.pujetid import add_pujetid_weight
from analysis.corrections.btag import BTagCorrector
from analysis.corrections.muon import MuonCorrector
from analysis.corrections.tau import TauCorrector
from analysis.corrections.electron import ElectronCorrector
from analysis.selections import (
    ObjectSelector,
    get_lumi_mask,
    get_trigger_mask,
    get_trigger_match_mask,
    get_metfilters_mask,
    get_stitching_mask,
)



class ZToJets(processor.ProcessorABC):
    def __init__(
        self,
        year: str = "2017",
        flow: str = "True",
    ):
        self.year = year
        self.flow = flow

        config_builder = ProcessorConfigBuilder(processor="ztojets", year=year)
        self.processor_config = config_builder.build_processor_config()
        self.histogram_config = self.processor_config.histogram_config
        self.histograms = HistBuilder(self.histogram_config).build_histogram()

        
    def process(self, events):
        year = self.year
        # get number of events
        nevents = len(events)
        # get dataset name
        dataset = events.metadata["dataset"]
        # check if sample is MC
        is_mc = hasattr(events, "genWeight")
        # get golden json, HLT paths and selections
        goldenjson = self.processor_config.goldenjson
        hlt_paths = self.processor_config.hlt_paths
        object_selections = self.processor_config.object_selection
        event_selections = self.processor_config.event_selection
        # create copies of histogram objects
        hist_dict = copy.deepcopy(self.histograms)
        # initialize output dictionary
        output = {}
        output["metadata"] = {}
        output["metadata"].update({"raw_initial_nevents": nevents})
        # define systematic variations shifts
        syst_variations = ["nominal"]
        for syst_var in syst_variations:
            # -------------------------------------------------------------
            # object corrections
            # -------------------------------------------------------------
            if is_mc:
                # apply JEC/JER corrections to jets (in data, the corrections are already applied)
                apply_jet_corrections(events, year)
                # apply energy corrections to taus (only to MC)
                apply_tau_energy_scale_corrections(
                    events=events, year=year, variation=syst_var
                )
            # apply rochester corretions to muons
            apply_rochester_corrections(
                events=events, is_mc=is_mc, year=year, variation=syst_var
            )
            # apply MET phi modulation corrections
            apply_met_phi_corrections(
                events=events,
                is_mc=is_mc,
                year=year,
            )
            # -------------------------------------------------------------
            # event SF/weights computation
            # -------------------------------------------------------------
            # set weights container
            weights_container = Weights(len(events), storeIndividual=True)
            if is_mc:
                # add gen weigths
                weights_container.add("genweight", events.genWeight)
                # add l1prefiring weigths
                add_l1prefiring_weight(events, weights_container, year, syst_var)
                # add pileup weigths
                add_pileup_weight(events, weights_container, year, syst_var)
                # add pujetid weigths
                add_pujetid_weight(
                    jets=events.Jet,
                    weights=weights_container,
                    year=year,
                    working_point=object_selections["jets"]["cuts"]["jets_pileup"],
                    variation=syst_var,
                )
                # b-tagging corrector
                btag_corrector = BTagCorrector(
                    events=events,
                    weights=weights_container,
                    sf_type="comb",
                    worging_point=object_selections["bjets"]["cuts"]["jets_deepjet"],
                    tagger="deepJet",
                    year=year,
                    full_run=False,
                    variation=syst_var,
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
                    id_working_point=object_selections["electrons"]["cuts"]["electrons_id"],
                )
                # add electron reco weights
                electron_corrector.add_reco_weight("RecoAbove20")
                electron_corrector.add_reco_weight("RecoBelow20")

                # muon corrector
                muon_corrector = MuonCorrector(
                    events=events,
                    weights=weights_container,
                    year=year,
                    variation=syst_var,
                    id_wp=object_selections["muons"]["cuts"]["muons_id"],
                    iso_wp=object_selections["muons"]["cuts"]["muons_iso"],
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
                    tau_vs_jet=object_selections["taus"]["cuts"]["taus_vs_jet"],
                    tau_vs_ele=object_selections["taus"]["cuts"]["taus_vs_ele"],
                    tau_vs_mu=object_selections["taus"]["cuts"]["taus_vs_mu"],
                    variation=syst_var,
                )
                tau_corrector.add_id_weight_deeptauvse()
                tau_corrector.add_id_weight_deeptauvsmu()
                tau_corrector.add_id_weight_deeptauvsjet()
            if syst_var == "nominal":
                # save sum of weights before object_selections
                output["metadata"].update({"sumw": ak.sum(weights_container.weight())})

            # -------------------------------------------------------------
            # object selection
            # -------------------------------------------------------------
            object_selector = ObjectSelector(object_selections, year)
            objects = object_selector.select_objects(events)

            # -------------------------------------------------------------
            # event selection
            # -------------------------------------------------------------
            event_selection = PackedSelection()
            for selection, str_mask in event_selections.items():
                event_selection.add(selection, eval(str_mask))

            region_cuts = event_selections.keys()
            region_selection = event_selection.all(*region_cuts)
            nevents_after = ak.sum(region_selection)

            if syst_var == "nominal":
                # save cutflow to metadata
                output["metadata"].update({"cutflow": {}})
                selections = []
                for cut_name in region_cuts:
                    selections.append(cut_name)
                    current_selection = event_selection.all(*selections)
                    output["metadata"]["cutflow"][cut_name] = ak.sum(
                        weights_container.weight()[current_selection]
                    )
                # save number of events after selection to metadata
                output["metadata"].update(
                    {
                        "weighted_final_nevents": ak.sum(
                            weights_container.weight()[region_selection]
                        ),
                        "raw_final_nevents": nevents_after,
                    }
                )
            # -------------------------------------------------------------
            # analysis features
            # -------------------------------------------------------------
            # check that there are events left after selection
            if nevents_after > 0:
                # get analysis features
                feature_map = {}
                for feature, axis_info in self.histogram_config.axes.items():
                    feature_map[feature] = eval(axis_info["expression"])[
                        region_selection
                    ]
                # -------------------------------------------------------------
                # histogram filling
                # -------------------------------------------------------------
                # break up the histogram filling for event-wise variations and object-wise variations
                # apply event-wise variations only for nominal
                if is_mc and syst_var == "nominal":
                    # get event weight systematic variations for MC samples
                    variations = ["nominal"] + list(weights_container.variations)
                    for variation in variations:
                        if variation == "nominal":
                            region_weight = weights_container.weight()[
                                region_selection
                            ]
                        else:
                            region_weight = weights_container.weight(
                                modifier=variation
                            )[region_selection]
                        fill_histogram(
                            histograms=hist_dict,
                            histogram_config=self.histogram_config,
                            feature_map=feature_map,
                            weights=region_weight,
                            variation=variation,
                            flow=self.flow,
                        )
                elif is_mc and syst_var != "nominal":
                    # object-wise variations
                    region_weight = weights_container.weight()[region_selection]
                    fill_histogram(
                        histograms=hist_dict,
                        histogram_config=self.histogram_config,
                        feature_map=feature_map,
                        weights=region_weight,
                        variation=syst_var,
                        flow=self.flow,
                    )
                elif not is_mc and syst_var == "nominal":
                    # object-wise variations
                    region_weight = weights_container.weight()[region_selection]
                    fill_histogram(
                        histograms=hist_dict,
                        histogram_config=self.histogram_config,
                        feature_map=feature_map,
                        weights=region_weight,
                        variation=syst_var,
                        flow=self.flow,
                    )
        # define output dictionary accumulator
        output["histograms"] = hist_dict
        return output

    def postprocess(self, accumulator):
        return accumulator
