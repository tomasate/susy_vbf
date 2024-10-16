import json
import vector
import numpy as np
import awkward as ak
import importlib.resources
from coffea.lumi_tools import LumiMask
from coffea.analysis_tools import PackedSelection
from analysis.helpers import working_points
from analysis.helpers.trigger import trigger_match


def object_selector(events, object_selection_config):
    # initialize dictionary to store analysis objects
    objects = {}
    for obj_name, obj_config in object_selection_config.items():
        # get object through field expression evaluation
        obj = eval(obj_config["field"])
        objects[obj_name] = obj
        if obj_config["cuts"]:
            # initialize selection mask
            selection_mask = ak.ones_like(obj.pt, dtype=bool)
            # iterate over all cuts
            for selection, str_mask in obj_config["cuts"].items():
                # if 'str_mask' contains 'events' or 'objects' evaluate the string expression
                # otherwise read the mask from the working points function
                if "events" in str_mask or "objects" in str_mask:
                    mask = eval(str_mask)
                else:
                    mask = getattr(working_points, selection)(events, str_mask)
                selection_mask = np.logical_and(selection_mask, mask)
            objects[obj_name] = objects[obj_name][selection_mask]
    return objects


def select_dimuons(muons):
    # create pair combinations with all muons
    dimuons = ak.combinations(muons, 2, fields=["mu1", "mu2"])
    # add dimuon 4-momentum field
    dimuons["p4"] = dimuons.mu1 + dimuons.mu2
    dimuons["pt"] = dimuons.p4.pt
    return dimuons


def select_dijets(jets):
    # create pair combinations with all jets (VBF selection)
    dijets = ak.combinations(jets, 2, fields=["j1", "j2"])
    # add dijet 4-momentum field
    dijets["p4"] = dijets.j1 + dijets.j2
    dijets["pt"] = dijets.p4.pt
    return dijets


def select_zerolepton_met(muons, met):
    # add muons pT to MET to simulate a 0-lepton final state
    all_muons = ak.sum(muons, axis=1)
    muons2D = ak.zip(
        {
            "pt": all_muons.pt,
            "phi": all_muons.phi,
        },
        with_name="Momentum2D",
        behavior=vector.backends.awkward.behavior,
    )
    met2D = ak.zip(
        {
            "pt": met.pt,
            "phi": met.phi,
        },
        with_name="Momentum2D",
        behavior=vector.backends.awkward.behavior,
    )
    return met2D + muons2D


def get_lumi_mask(events, lumimask, is_mc):
    if is_mc:
        lumi_mask = np.ones(len(events), dtype="bool")
    else:
        lumi_info = LumiMask(lumimask)
        lumi_mask = lumi_info(events.run, events.luminosityBlock)
    return lumi_mask


def get_trigger_mask(events, hlt_paths):
    trigger_mask = np.zeros(len(events), dtype="bool")
    trigger_match_mask = np.zeros(len(events), dtype="bool")
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


def get_metfilters_mask(events, is_mc, year):
    with importlib.resources.path("analysis.data", "metfilters.json") as path:
        with open(path, "r") as handle:
            metfilters = json.load(handle)[year]
    metfilters_mask = np.ones(len(events), dtype="bool")
    metfilterkey = "mc" if is_mc else "data"
    for mf in metfilters[metfilterkey]:
        if mf in events.Flag.fields:
            metfilters_mask = metfilters_mask & events.Flag[mf]
    return metfilters_mask


def get_stitching_mask(events, dataset, dataset_key, ht_value):
    stitching_mask = np.ones(len(events), dtype="bool")
    if dataset.startswith(dataset_key):
        stitching_mask = events.LHE.HT < ht_value
    return stitching_mask
