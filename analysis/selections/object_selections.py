import vector
import inspect
import numpy as np
import awkward as ak
from analysis.working_points import working_points
from analysis.corrections.jetvetomaps import jetvetomaps_mask


def delta_r_mask(first, second, threshold=0.4):
    """select objects from 'first' which are at least 'threshold' away from all objects in 'second'."""
    mval = first.metric_table(second)
    return ak.all(mval > threshold, axis=-1)


class ObjectSelector:

    def __init__(self, object_selection_config, year):
        self.year = year
        self.object_selection_config = object_selection_config

    def select_objects(self, events):
        self.objects = {}
        self.events = events
        for obj_name, obj_config in self.object_selection_config.items():
            # check if object field is read from events or from user defined function
            if "events" in obj_config["field"]:
                self.objects[obj_name] = eval(obj_config["field"])
            else:
                selection_function = getattr(self, obj_config["field"])
                parameters = inspect.signature(selection_function).parameters.keys()
                if "cuts" in parameters:
                    selection_function(obj_config["cuts"])
                    break
                else:
                    selection_function()
            if "cuts" in obj_config:
                selection_mask = self.get_selection_mask(
                    events=events, obj_name=obj_name, cuts=obj_config["cuts"]
                )
                self.objects[obj_name] = self.objects[obj_name][selection_mask]
        return self.objects

    def get_selection_mask(self, events, obj_name, cuts):
        # bring 'objects' and to local scope
        objects = self.objects
        # initialize selection mask
        selection_mask = ak.ones_like(self.objects[obj_name].pt, dtype=bool)
        # iterate over all cuts
        for selection, str_mask in cuts.items():
            # cast 'str_mask' to str if needed
            # for instance: 'taus_decaymode: 13'
            if not isinstance(str_mask, str):
                str_mask = str(str_mask)
            # check if 'str_mask' contains 'events' or 'objects'
            if "events" in str_mask or "objects" in str_mask:
                # evaluate string expression for the mask
                mask = eval(str_mask)
            else:
                # load working point function
                wp_function = getattr(working_points, selection)
                # get working point function parameters
                signature = inspect.signature(wp_function)
                parameters = signature.parameters.keys()
                args_map = {
                    "events": self.events,
                    "wp": str_mask,
                    "year": self.year,
                }
                args = {}
                for param in parameters:
                    if param in args_map:
                        args[param] = args_map[param]
                    else:
                        args[param] = cuts[param]
                # get mask from working point function
                mask = wp_function(**args)
            # update selection mask
            selection_mask = np.logical_and(selection_mask, mask)
        return selection_mask

    def select_dijets(self):
        # create pair combinations with all jets (VBF selection)
        dijets = ak.combinations(self.objects["jets"], 2, fields=["j1", "j2"])
        # add dijet 4-momentum field
        dijets["p4"] = dijets.j1 + dijets.j2
        dijets["pt"] = dijets.p4.pt
        self.objects["dijets"] = dijets

    def select_dimuons(self):
        # create pair combinations with all muons
        dimuons = ak.combinations(self.objects["muons"], 2, fields=["mu1", "mu2"])
        # add dimuon 4-momentum field
        dimuons["p4"] = dimuons.mu1 + dimuons.mu2
        dimuons["pt"] = dimuons.p4.pt
        self.objects["dimuons"] = dimuons

    def select_met(self):
        # add muons pT to MET to simulate a 0-lepton final state
        all_muons = ak.sum(self.objects["muons"], axis=1)
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
                "pt": self.events.MET.pt,
                "phi": self.events.MET.phi,
            },
            with_name="Momentum2D",
            behavior=vector.backends.awkward.behavior,
        )
        self.objects["met"] = met2D + muons2D
