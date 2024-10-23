import numpy as np
import awkward as ak

class WorkingPoints:
    
    def muons_id(self, events, wp):
        wps = {
            "highpt": events.Muon.highPtId == 2,
            # cutbased ID working points
            "loose": events.Muon.looseId,
            "medium": events.Muon.mediumId,
            "tight": events.Muon.tightId,
        }
        return wps[wp]
    
    def muons_iso(self, events, wp):
        wps = {
            "loose": (
                events.Muon.pfRelIso04_all < 0.25
                if hasattr(events.Muon, "pfRelIso04_all")
                else events.Muon.pfRelIso03_all < 0.25
            ),
            "medium": (
                events.Muon.pfRelIso04_all < 0.20
                if hasattr(events.Muon, "pfRelIso04_all")
                else events.Muon.pfRelIso03_all < 0.20
            ),
            "tight": (
                events.Muon.pfRelIso04_all < 0.15
                if hasattr(events.Muon, "pfRelIso04_all")
                else events.Muon.pfRelIso03_all < 0.15
            ),
        }
        return wps[wp]
    
    def electrons_id(self, events, wp):
        wps = {
            # mva ID working points https://twiki.cern.ch/twiki/bin/view/CMS/MultivariateElectronIdentificationRun2
            "wp80iso": events.Electron.mvaFall17V2Iso_WP80,
            "wp90iso": events.Electron.mvaFall17V2Iso_WP90,
            "wp80noiso": events.Electron.mvaFall17V2noIso_WP80,
            "wp90noiso": events.Electron.mvaFall17V2noIso_WP90,
            # cutbased ID working points https://twiki.cern.ch/twiki/bin/view/CMS/CutBasedElectronIdentificationRun2
            "loose": events.Electron.cutBased == 2,
            "medium": events.Electron.cutBased == 3,
            "tight": events.Electron.cutBased == 4,
        }
        return wps[wp]
    
    def electrons_iso(self, events, wp):
        wps = {
            # https://twiki.cern.ch/twiki/bin/view/CMS/SWGuideMuonSelection
            "loose": events.Electron.pfRelIso04_all < 0.25
            if hasattr(events.Electron, "pfRelIso04_all")
            else events.Electron.pfRelIso03_all < 0.25,
            "medium": events.Electron.pfRelIso04_all < 0.20
            if hasattr(events.Electron, "pfRelIso04_all")
            else events.Electron.pfRelIso03_all < 0.20,
            "tight": events.Electron.pfRelIso04_all < 0.15
            if hasattr(events.Electron, "pfRelIso04_all")
            else events.Electron.pfRelIso03_all < 0.15,
        }
        return wps[wp]
    
    def taus_vs_jet(self, events, wp):
        wps = {
            "vvvloose": events.Tau.idDeepTau2017v2p1VSjet > 1,
            "vvloose": events.Tau.idDeepTau2017v2p1VSjet > 2,
            "vloose": events.Tau.idDeepTau2017v2p1VSjet > 4,
            "loose": events.Tau.idDeepTau2017v2p1VSjet > 8,
            "medium": events.Tau.idDeepTau2017v2p1VSjet > 16,
            "tight": events.Tau.idDeepTau2017v2p1VSjet > 32,
            "vtight": events.Tau.idDeepTau2017v2p1VSjet > 64,
            "vvtight": events.Tau.idDeepTau2017v2p1VSjet > 128
        }
        return wps[wp]
    
    def taus_vs_ele(self, events, wp):
        wps = {
            "vvvloose": events.Tau.idDeepTau2017v2p1VSe > 1,
            "vvloose": events.Tau.idDeepTau2017v2p1VSe > 2,
            "vloose": events.Tau.idDeepTau2017v2p1VSe > 4,
            "loose": events.Tau.idDeepTau2017v2p1VSe > 8,
            "medium": events.Tau.idDeepTau2017v2p1VSe > 16,
            "tight": events.Tau.idDeepTau2017v2p1VSe > 32,
            "vtight": events.Tau.idDeepTau2017v2p1VSe > 64,
            "vvtight": events.Tau.idDeepTau2017v2p1VSe > 128
        }
        return wps[wp]
    
    def taus_vs_mu(self, events, wp):
        wps = {
            "vloose": events.Tau.idDeepTau2017v2p1VSmu > 1,
            "loose": events.Tau.idDeepTau2017v2p1VSmu > 2,
            "medium": events.Tau.idDeepTau2017v2p1VSmu > 4,
            "tight": events.Tau.idDeepTau2017v2p1VSmu > 8
        }
        return wps[wp]
    
    def tau_decaymode(self, events, wp):
        prong_to_modes = {
            "1": [0, 1, 2],
            "2": [5, 6, 7],
            "3": [10, 11],
            "13": [0, 1, 2, 10, 11],
            "12": [0, 1, 2, 5, 6, 7],
            "23": [5, 6, 7, 10, 11],
        }
        if wp not in prong_to_modes:
            raise ValueError(
                "Invalid prong value. Please specify 1, 2, 3, 12, 13 or 23 for the prong parameter."
            )
        tau_dm = events.Tau.decayMode
        decay_mode_mask = ak.zeros_like(tau_dm)
        for mode in prong_to_modes[wp]:
            decay_mode_mask = np.logical_or(decay_mode_mask, tau_dm == mode)
        return decay_mode_mask
        
    
    def jets_pileup(self, events, wp, year):
        puid_wps = {
            "2016preVFP": {
                "loose": events.Jet.puId == 1,
                "medium": events.Jet.puId == 3,
                "tight": events.Jet.puId == 7,
            },
            "2016postVFP": {
                "loose": events.Jet.puId == 1,
                "medium": events.Jet.puId == 3,
                "tight": events.Jet.puId == 7,
            },
            "2017": {
                "loose": events.Jet.puId == 4,
                "medium": events.Jet.puId == 6,
                "tight": events.Jet.puId == 7,
            },
            "2018": {
                "loose": events.Jet.puId == 4,
                "medium": events.Jet.puId == 6,
                "tight": events.Jet.puId == 7,
            }
        }
        return puid_wps[year][wp]
        
    def jets_deepjet(self, events, wp, year):
        
        wps = {
            "2016preVFP": {
                "loose": events.Jet.btagDeepFlavB > 0.0508,
                "medium": events.Jet.btagDeepFlavB > 0.2598,
                "tight": events.Jet.btagDeepFlavB > 0.6502
            },
            "2016postVFP": {
                "loose": events.Jet.btagDeepFlavB > 0.048,
                "medium": events.Jet.btagDeepFlavB > 0.2489,
                "tight": events.Jet.btagDeepFlavB > 0.6377
            },
            "2017": {
                "loose": events.Jet.btagDeepFlavB > 0.0532,
                "medium": events.Jet.btagDeepFlavB > 0.304,
                "tight": events.Jet.btagDeepFlavB > 0.7476
            },
            "2018": {
                "loose": events.Jet.btagDeepFlavB > 0.049,
                "medium": events.Jet.btagDeepFlavB > 0.2783,
                "tight": events.Jet.btagDeepFlavB > 0.71
            }
        }
        return wps[year][wp]
        