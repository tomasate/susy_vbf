import vector
import inspect
import numpy as np
import awkward as ak
from analysis.working_points import working_points
from analysis.corrections.jetvetomaps import jetvetomaps_mask


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
                if "cuts" in obj_config:
                    cuts = obj_config["cuts"]
                    selection_mask = self.get_selection_mask(events=events, obj_name=obj_name, cuts=cuts)
                    self.objects[obj_name] = self.objects[obj_name][selection_mask]
            else:
                selection_function = getattr(self, obj_config["field"])
                if "cuts" in obj_config:
                    selection_function(obj_config["cuts"])
                else:
                    selection_function()
                
        return self.objects
    
    
    def get_selection_mask(self, events, obj_name, cuts):
        # initialize selection mask
        selection_mask = ak.ones_like(self.objects[obj_name].pt, dtype=bool)
        # iterate over all cuts
        for selection, str_mask in cuts.items():
            # check if jet veto maps
            if selection == "jetsvetomaps":
                if str_mask:
                    mask = jetvetomaps_mask(events.Jet, year=self.year)
            # check if selections is cross-cleaning
            elif "dr" in selection:
                mask = self.delta_r_mask(selection=selection, threshold=str_mask)
            # check if 'str_mask' contains 'events' or 'objects' and evaluate string expression
            elif "events" in str_mask or "objects" in str_mask:
                mask = eval(str_mask)
            # read the mask from the working points function
            else:
                signature = inspect.signature(getattr(working_points, selection))
                parameters = signature.parameters.keys()
                if "year" in parameters:
                    mask = getattr(working_points, selection)(self.events, str_mask, self.year)
                else:
                    mask = getattr(working_points, selection)(self.events, str_mask)
                    
            # update selection mask
            selection_mask = np.logical_and(selection_mask, mask)
        
        return selection_mask
             
        
    def select_jets(self, cuts):
        # break up selection for low and high pT jets
        # to apply jets_pileup only to jets with pT < 50 GeV
        low_pt_jets_mask = (
            (self.events.Jet.pt > cuts["min_pt"])
            & (self.events.Jet.pt < 50)
            & working_points.jets_pileup(self.events, cuts["jets_pileup"], self.year)
        )
        high_pt_jets_mask = (
            (self.events.Jet.pt > 50)
        )
        selection_mask = ak.where(
            (self.events.Jet.pt > cuts["min_pt"]) & (self.events.Jet.pt < 50),
            low_pt_jets_mask,
            high_pt_jets_mask,
        )
        selection_mask = (
            selection_mask
            & (np.abs(self.events.Jet.eta) < cuts["eta"])
            & working_points.jets_id(self.events, cuts["jets_id"])
        )
        # apply jet veto maps
        if cuts["jetsvetomaps"]:
            selection_mask = selection_mask & jetvetomaps_mask(self.events.Jet, self.year)
        # cross-cleaning wiht leptons
        dr_values = ["jets_electrons_dr", "jets_muons_dr", "jets_taus_dr"]
        for dr in dr_values:
            if dr in cuts:
                selection_mask = (
                    selection_mask
                    & (self.delta_r_mask(dr, cuts[dr]))
                )
        # apply object selection cuts
        self.objects["jets"] = self.events.Jet[selection_mask]


    def select_dijets(self, cuts):
        # create pair combinations with all jets (VBF selection)
        dijets = ak.combinations(self.objects["jets"], 2, fields=["j1", "j2"])
        # add dijet 4-momentum field
        dijets["p4"] = dijets.j1 + dijets.j2
        
        # apply object selection cuts
        selection_mask = (
            (np.abs(dijets.j1.eta - dijets.j2.eta) > cuts['delta_eta'])
            & (dijets.j1.eta * dijets.j2.eta < 0)
            & (dijets.p4.mass > cuts['max_mass'])
        )
        self.objects["dijets"] = dijets[selection_mask]
    
    
    def select_dimuons(self, cuts):
        # create pair combinations with all muons
        dimuons = ak.combinations(self.objects["muons"], 2, fields=["mu1", "mu2"])
        # add dimuon 4-momentum field
        dimuons["p4"] = dimuons.mu1 + dimuons.mu2

        # apply object selection cuts
        selection_mask = (
            (dimuons.mu1.charge * dimuons.mu2.charge < 0)
            & (dimuons.p4.mass > cuts["min_mass"]) & (dimuons.p4.mass < cuts["max_mass"])
        )
        self.objects["dimuons"] = dimuons[selection_mask]
    
    
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
    
    
    def delta_r_mask(self, selection, threshold) -> ak.Array:
        first_objects_map = {
            "electrons": self.events.Electron,
            "muons": self.events.Muon,
            "taus": self.events.Tau,
            "jets": self.events.Jet
        }
        second_objects_map = {obj_name: self.objects[obj_name] for obj_name in self.objects}
        # read first and second objects from 'first_second_dr' selection string
        first, second, _ = selection.split("_")
        # select objects from 'first' which are at least threshold away from all objects in 'second'.
        mval = first_objects_map[first].metric_table(second_objects_map[second])
        return ak.all(mval > threshold, axis=-1)