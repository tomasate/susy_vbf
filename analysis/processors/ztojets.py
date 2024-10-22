import json
import copy
import pickle
import numpy as np
import awkward as ak
import importlib.resources
from coffea import processor
from coffea.analysis_tools import PackedSelection, Weights
from analysis.configs import load_config
from analysis.histograms import HistBuilder, fill_histogram
from analysis.selections import (
    object_selector,
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

        self.processor_config = load_config(
            config_type="processor", config_name="ztojets", year="2017"
        )
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
        # get lumimask
        goldenjson = self.processor_config.goldenjson
        hlt_paths = self.processor_config.hlt_paths
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
            # TO DO
            # -------------------------------------------------------------
            # event SF/weights computation
            # -------------------------------------------------------------
            # set weights container
            weights_container = Weights(len(events), storeIndividual=True)
            if is_mc:
                # add gen weigths
                weights_container.add("genweight", events.genWeight)

            if syst_var == "nominal":
                # save sum of weights before selections
                output["metadata"].update({"sumw": ak.sum(weights_container.weight())})

            # -------------------------------------------------------------
            # object selection
            # -------------------------------------------------------------
            objects = object_selector(events, self.processor_config.object_selection)

            # -------------------------------------------------------------
            # event selection
            # -------------------------------------------------------------
            event_selection = PackedSelection()
            for selection, str_mask in self.processor_config.event_selection.items():
                event_selection.add(selection, eval(str_mask))

            region_cuts = self.processor_config.event_selection.keys()
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
            # event features
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
                if self.output_type == "hist":
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
                            variation=variation,
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
                            variation=variation,
                            flow=self.flow,
                        )
        # define output dictionary accumulator
        output["histograms"] = hist_dict
        return output

    def postprocess(self, accumulator):
        return accumulator
