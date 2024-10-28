import numpy as np
from analysis.configs.processor_config import ProcessorConfig
from analysis.configs.histogram_config import HistogramConfig


processor_config = ProcessorConfig(
    goldenjson="analysis/data/Cert_271036-284044_13TeV_Legacy2016_Collisions16_JSON.txt",
    hlt_paths=["IsoMu24"],
    object_selection={
        "muons": {
            "field": "events.Muon",
            "cuts": {
                "pt": "events.Muon.pt > 30",
                "eta": "np.abs(events.Muon.eta) < 2.4",
                "muons_id": "tight",
                "muons_iso": "tight",
            }
        },
        "veto_muons": {
            "field": "events.Muon",
            "cuts": {
                "min_pt": "events.Muon.pt > 3",
                "max_pt": "events.Muon.pt < 30",
                "eta": "np.abs(events.Muon.eta) < 2.1",
                "muons_id": "tight",
                "muons_iso": "tight",
            }
        },
        "electrons": {
            "field": "events.Electron",
            "cuts": {
                "pt": "events.Electron.pt > 30",
                "eta": "np.abs(events.Electron) < 2.1",
                "electrons_id": "wp80iso",
            }
        },
        "taus": {
            "field": "events.Tau",
            "cuts": {
                "pt": "events.Tau.pt > 20",
                "eta": "np.abs(events.Tau.eta) < 2.1",
                "dz": "np.abs(events.Tau.dz) < 0.2",
                "taus_vs_jet": "loose",
                "taus_vs_ele": "vvloose",
                "taus_vs_mu": "loose",
                "tau_decaymode": "13",
            }
        },
        "jets": {
            "field": "events.Jet",
            "cuts": {
                "pt": "events.Jet.pt > 30",
                "eta": "np.abs(events.Jet) < 4.7",
                "jets_pileup": "tight",
                "jets_id": "loose",
            }
        },
        "bjets": {
            "field": "events.Jet",
            "cuts": {
                "pt": "events.Jet.pt > 30",
                "eta": "np.abs(events.Jet) < 2.4",
                "jets_pileup": "tight",
                "id": "events.Jet.jetId == 6",
                "jets_deepjet": "medium",
            }
        },
        "met": {
            "field": "events.MET",
            "cuts": None
        },
        "zerolepton_met": {
            "field": "select_zerolepton_met(objects['muons'], objects['met'])",
            "cuts": None
        },
        "dimuons": {
            "field": "select_dimuons(objects['muons'])",
            "cuts": {
                "mass_range": "(objects['dimuons'].p4.mass > 60) & (objects['dimuons'].p4.mass < 120)",
                "opp_charge": "objects['dimuons'].mu1.charge * objects['dimuons'].mu2.charge < 0"
            }
        },
        "dijets": {
            "field": "select_dijets(objects['jets'])",
            "cuts": {
                "delta_eta": "np.abs(objects['dijets'].j1.eta - objects['dijets'].j2.eta) > 3.8",
                "opp_charge": "objects['dijets'].j1.eta * objects['dijets'].j2.eta < 0",
                "mass": "(objects['dijets'].p4.mass > 500)"
            }
        }
    },
    event_selection={
        "goodvertex": "events.PV.npvsGood > 0",
        "lumi": "get_lumi_mask(events, goldenjson, is_mc)",
        "trigger": "get_trigger_mask(events, hlt_paths)",
        "trigger_match": "get_trigger_match_mask(events, hlt_paths)",
        "metfilters": "get_metfilters_mask(events, is_mc, year)",
        "dy_stitching": "get_stitching_mask(events, dataset, 'DYJetsToLL_inclusive', 70)",
        "w_stitching": "get_stitching_mask(events, dataset, 'WJetsToLNu_inclusive', 100)",
        "0lstate": "objects['zerolepton_met'].pt > 250",
        "two_muons": "ak.num(objects['muons']) == 2",
        "one_dimuon": "ak.num(objects['dimuons']) == 1",
        "muon_veto": "ak.num(objects['veto_muons']) == 0",
        "electron_veto": "ak.num(objects['electrons']) == 0",
        "tau_veto": "ak.num(objects['taus']) == 0",
        "bjet_veto": "ak.num(objects['bjets']) == 0",
        "atleast_two_jets": "ak.num(objects['jets']) > 1",
        "atleast_one_dijet": "ak.num(objects['dijets']) > 0",
    },
    histogram_config=HistogramConfig(
        add_syst_axis=True,
        add_weight=True,
        add_cat_axis=None,
        axes={
            "muon_pt": {
                "type": "Variable",
                "edges": [30, 60, 90, 120, 150, 180, 210, 240, 300, 500],
                "label": r"$p_T(\mu)$ [GeV]",
                "expression": "objects['muons'].pt"
            },
            "muon_eta": {
                "type": "Regular",
                "bins": 50,
                "start": -2.4,
                "stop": 2.4,
                "label": "$\eta(\mu)$",
                "expression": "objects['muons'].eta"
            },
            "muon_phi": {
                "type": "Regular",
                "bins": 50,
                "start": -np.pi,
                "stop": np.pi,
                "label": "$\phi(\mu)$",
                "expression": "objects['muons'].phi"
            },
            "dimuon_mass": {
                "type": "Regular",
                "bins": 24,
                "start": 60,
                "stop": 120,
                "label": r"$m(\mu \mu)$ [GeV]",
                "expression": "objects['dimuons'].p4.mass"
            },
            "dimuon_pt": {
                "type": "Regular",
                "bins": 50,
                "start": 0,
                "stop": 1000,
                "label": r"$p_T(\mu \mu)$ [GeV]",
                "expression": "objects['dimuons'].p4.pt"
            },
            "jet_pt": {
                "type": "Variable",
                "edges": [20, 60, 90, 120, 150, 180, 210, 240, 300, 500],
                "label": r"$p_T(j)$ [GeV]",
                "expression": "objects['jets'].pt"
            },
            "jet_eta": {
                "type": "Regular",
                "bins": 50,
                "start": -4.7,
                "stop": 4.7,
                "label": "$\eta(j)$",
                "expression": "objects['jets'].eta"
            },
            "dijet_mass": {
                "type": "Variable",
                "edges": [500, 600, 800, 1000, 1200, 1400, 1600, 1800, 2000, 2200, 2400, 2600, 2800, 3200, 3800, 5000],
                "label": r"Largest $m(jj)$ [GeV]",
                "expression": "ak.max(objects['dijets'].p4.mass, axis=1)"
            },
            "zerolepton_met": {
                "type": "Variable",
                "edges": [250, 260, 270, 280, 290, 300, 320, 340, 360, 380, 400, 450, 500, 1000],
                "label": r"$p_T^{miss}$ [GeV]",
                "expression": "objects['zerolepton_met'].pt"
            },
        },
        layout={
            "muons": ["muon_pt", "muon_eta", "muon_phi"],
            "dimuons": ["dimuon_pt", "dimuon_mass"],
            "jets": ["jet_pt", "jet_eta"],
            "dijets": ["dijet_mass"],
            "zerolepton_met": ["zerolepton_met"]
        }
    )
)