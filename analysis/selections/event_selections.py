import json
import numpy as np
import awkward as ak
import importlib.resources
from coffea.lumi_tools import LumiMask
from analysis.selections import trigger_match


def get_metfilters_mask(events, year):
    with importlib.resources.path("analysis.data", "metfilters.json") as path:
        with open(path, "r") as handle:
            metfilters = json.load(handle)[year]
    metfilters_mask = np.ones(len(events), dtype="bool")
    metfilterkey = "mc" if hasattr(events, "genWeight") else "data"
    for mf in metfilters[metfilterkey]:
        if mf in events.Flag.fields:
            metfilters_mask = metfilters_mask & events.Flag[mf]
    return metfilters_mask


def get_lumi_mask(events, lumimask):
    if hasattr(events, "genWeight"):
        lumi_mask = np.ones(len(events), dtype="bool")
    else:
        lumi_info = LumiMask(lumimask)
        lumi_mask = lumi_info(events.run, events.luminosityBlock)
    return lumi_mask


def get_trigger_mask(events, hlt_paths):
    trigger_mask = np.zeros(len(events), dtype="bool")
    
    for hlt_path in hlt_paths:
        if hlt_path in events.HLT.fields:
            trigger_mask = trigger_mask | events.HLT[hlt_path]
    return trigger_mask


def get_trigger_match_mask(events, hlt_paths, lepton="Muon"):
    trigger_match_mask = np.zeros(len(events), dtype="bool")
    for hlt_path in hlt_paths:
        trig_match = trigger_match(
            leptons=events[lepton],
            trigobjs=events.TrigObj,
            trigger_path=hlt_path,
        )
        trigger_match_mask = trigger_match_mask | trig_match
    return ak.sum(trigger_match_mask, axis=-1) > 0


def get_stitching_mask(events, dataset, dataset_key, ht_value):
    stitching_mask = np.ones(len(events), dtype="bool")
    if dataset.startswith(dataset_key):
        stitching_mask = events.LHE.HT < ht_value
    return stitching_mask