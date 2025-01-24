import yaml
import correctionlib
import numpy as np
import awkward as ak
from pathlib import Path
from coffea.nanoevents.methods import candidate
from analysis.corrections.met import corrected_polar_met
from analysis.corrections.utils import get_pog_json, get_jer_cset, get_era
from analysis.selections.object_selections import delta_r_mask


class JERCorrector:

    def __init__(
        self,
        events,
        year,
        dataset,
        apply_jec,
        apply_jer,
        apply_jec_syst=False,
        apply_jer_syst=False,
    ):
        self.events = events
        self.year = year
        self.era = get_era(dataset)
        self.apply_jec = apply_jec
        self.apply_jer = apply_jer
        self.apply_jec_syst = apply_jec_syst
        self.apply_jer_syst = apply_jer_syst

        # load jerc data
        jerc_data_path = Path.cwd() / "analysis" / "data"
        with open(f"{jerc_data_path}/jerc.yaml", "r") as f:
            self.jerc_data = yaml.safe_load(f)

        # prepare input variables
        self.events["Jet", "pt_raw"] = self.events.Jet.pt * (
            1 - self.events.Jet.rawFactor
        )
        self.events["Jet", "mass_raw"] = self.events.Jet.mass * (
            1 - self.events.Jet.rawFactor
        )
        try:
            self.events["Jet", "rho"] = (
                ak.ones_like(self.events.Jet.pt) * self.events.fixedGridRhoFastjetAll
            )
        except:
            self.events["Jet", "rho"] = (
                ak.ones_like(self.events.Jet.pt)
                * self.events.Rho.fixedGridRhoFastjetAll
            )
        if self.apply_jer:
            self.events["Jet", "pt_gen"] = ak.values_astype(
                ak.fill_none(self.events.Jet.matched_gen.pt, 0), np.float32
            )
            self.events["Jet", "event_id"] = (
                ak.ones_like(self.events.Jet.pt) * self.events.event
            )

        # apply jec/jer corrections
        if self.apply_jec:
            self.apply_jec_corr()
            self.apply_met_t1_corr()
        if self.apply_jer:
            self.apply_jer_corr()
            self.apply_met_jer_corr()
        if self.apply_jec_syst:
            self.apply_jec_syst_corr()

    def apply_jec_corr(self):
        self.events["Jet", "idx"] = ak.local_index(self.events.Jet, axis=1)
        # get jec compound scale factor
        compound_sf = self.get_jec_sf(level="compound")
        # get jec pT and mass
        self.events["Jet", "pt_jec"] = compound_sf * self.events.Jet.pt_raw
        self.events["Jet", "mass_jec"] = compound_sf * self.events.Jet.mass_raw
        # update nominal pT and mass
        self.events["Jet", "pt"] = self.events.Jet.pt_jec
        self.events["Jet", "mass"] = self.events.Jet.mass_jec

    def apply_jec_syst_corr(self):
        sf_delta = self.get_jec_sf(level="uncert")
        # divide by correction since it is already applied before
        corr_up_variation = 1 + sf_delta
        corr_down_variation = 1 - sf_delta
        self.events["Jet", "pt_jec_up"] = self.events.Jet.pt * corr_up_variation
        self.events["Jet", "pt_jec_down"] = self.events.Jet.pt * corr_down_variation
        self.events["Jet", "mass_jec_up"] = self.events.Jet.mass * corr_up_variation
        self.events["Jet", "mass_jec_down"] = self.events.Jet.mass * corr_down_variation

    def apply_jer_corr(self):
        # get jer scale factor
        smearing = self.get_jer_sf("nom")
        # check that smeared jet energy remains positive as the direction of the jet would change otherwise
        smearing_pt = ak.where(
            smearing * self.events.Jet.E < 0.01, 0.01 / self.events.Jet.E, smearing
        )
        smearing_mass = ak.where(
            smearing * self.events.Jet.mass_jec < 0.01, 0.01, smearing
        )
        # set jer pT and mass
        self.events["Jet", "pt_jer"] = smearing_pt * self.events.Jet.pt_jec
        self.events["Jet", "mass_jer"] = smearing_mass * self.events.Jet.mass_jec
        # update nominal pT and mass
        self.events["Jet", "pt"] = self.events.Jet.pt_jer
        self.events["Jet", "mass"] = self.events.Jet.mass_jer
        # get jer variations
        if self.apply_jer_syst:
            for variation in ["up", "down"]:
                smearing_variation = self.get_jer_sf(variation)
                # check that smeared jet energy remains positive as the direction of the jet would change otherwise
                smearing_pt = ak.where(
                    smearing_variation * self.events.Jet.E < 0.01,
                    0.01 / self.events.Jet.E,
                    smearing_variation,
                )
                smearing_mass = ak.where(
                    smearing_variation * self.events.Jet.mass_jec < 0.01,
                    0.01,
                    smearing_variation,
                )
                self.events["Jet", f"pt_jer_{variation}"] = (
                    smearing_variation * self.events.Jet.pt_jec
                )
                self.events["Jet", f"mass_jer_{variation}"] = (
                    smearing_variation * self.events.Jet.mass_jec
                )

    def get_jec_sf(self, level: str):
        """
        returns scale factors for a given level/era

        Parameters:
        -----------
            level:
                jec level {L1, L2, L3, compound}
        """
        # get correction set
        cset = correctionlib.CorrectionSet.from_file(get_pog_json("jerc", self.year))
        if level == "compound":
            cset = cset.compound
        # get correction file name by jec level and era
        jec_corr_key = "_".join(
            [
                self.jerc_data["jec_version"][self.year][self.era],
                self.jerc_data["jec_level"][level],
                self.jerc_data["algorithm"][self.year],
            ]
        )
        # flatten jagged array
        jets = ak.flatten(self.events.Jet)
        # get input variables
        input_variables = [
            jets[self.jerc_data["jec_input_map"][level][i.name]]
            for i in cset[jec_corr_key].inputs
        ]
        # return level correction SF
        sf = cset[jec_corr_key].evaluate(*input_variables)
        return ak.unflatten(sf, ak.num(self.events.Jet))

    def get_jer_sf(self, variation: str):
        """
        returns jer scale factor

        Parameters:
        -----------
            variation: systematic variation {nom, up, down}
        """
        # flatten jagged array
        jets = ak.flatten(self.events.Jet)
        # get jer correction set
        jer_tag = self.jerc_data["jer_version"][self.year]
        jer_ptres_tag = (
            f"{jer_tag}_PtResolution_{self.jerc_data['algorithm'][self.year]}"
        )
        jer_sf_tag = f"{jer_tag}_ScaleFactor_{self.jerc_data['algorithm'][self.year]}"
        cset = get_jer_cset(jer_ptres_tag, jer_sf_tag, self.year)
        # get jer pt resolution
        jer_ptres = cset[jer_ptres_tag].evaluate(jets.eta, jets.pt_jec, jets.rho)
        # adjust gen pT
        ptgen = np.where(
            np.abs(jets.pt_jec - jets.pt_gen) < 3 * jets.pt_jec * jer_ptres,
            jets.pt_gen,
            -1.0,
        )
        # get jer scale factor
        jersf = cset[jer_sf_tag].evaluate(jets.eta, variation)
        jersmear = cset["JERSmear"].evaluate(
            jets.pt_jec, jets.eta, ptgen, jets.rho, jets.event_id, jer_ptres, jersf
        )
        return ak.unflatten(jersmear, ak.num(self.events.Jet))

    def get_jets_for_met_t1(self):
        """
        return L123 and L1 jets needed for type-I MET corrections
        """
        # get L1, L2 and L3 jets pT
        l1_sf = self.get_jec_sf(level="L1")
        self.events["Jet", "pt_l1"] = l1_sf * self.events.Jet.pt_raw

        l2_sf = self.get_jec_sf(level="L2")
        self.events["Jet", "pt_l12"] = l2_sf * self.events.Jet.pt_l1

        l3_sf = self.get_jec_sf(level="L3")
        self.events["Jet", "pt_l123"] = l3_sf * self.events.Jet.pt_l12

        # get L123 and L1 jets components
        pt_raw_x = self.events.Jet.pt_raw * np.cos(self.events.Jet.phi)
        pt_raw_y = self.events.Jet.pt_raw * np.sin(self.events.Jet.phi)

        jet_x_L123 = l1_sf * l2_sf * l3_sf * pt_raw_x
        jet_y_L123 = l1_sf * l2_sf * l3_sf * pt_raw_y

        jet_x_L1 = l1_sf * pt_raw_x
        jet_y_L1 = l1_sf * pt_raw_y

        jet_pt_L123 = np.sqrt((jet_x_L123**2.0 + jet_y_L123**2.0))
        jet_phi_L123 = np.arctan2(jet_x_L123, jet_y_L123)

        jet_pt_L1 = np.sqrt((jet_x_L1**2.0 + jet_y_L1**2.0))
        jet_phi_L1 = np.arctan2(jet_x_L1, jet_y_L1)

        # define L123 and L1 jets
        jets_L123 = ak.zip(
            {
                "pt": jet_pt_L123,
                "phi": jet_phi_L123,
                "eta": self.events.Jet.eta,
                "mass": self.events.Jet.mass,
            },
            with_name="PtEtaPhiMCandidate",
            behavior=candidate.behavior,
        )
        jets_L1 = ak.zip(
            {
                "pt": jet_pt_L1,
                "phi": jet_phi_L1,
                "eta": self.events.Jet.eta,
                "mass": self.events.Jet.mass,
            },
            with_name="PtEtaPhiMCandidate",
            behavior=candidate.behavior,
        )
        return jets_L123, jets_L1

    def apply_met_t1_corr(self):
        """
        Apply MET type-I correction (Propagation of Jet Energy Scale Corrections)

        Documentation:
        https://twiki.cern.ch/twiki/bin/viewauth/CMS/MissingETRun2Corrections#Type_I_Correction_Propagation_of
        https://twiki.cern.ch/twiki/bin/view/CMS/METType1Type2Formulae#3_The_Type_I_correction
        """
        # get jets to correct type-I MET
        jets_L123, jets_L1 = self.get_jets_for_met_t1()
        # The jet collection used in Type-I corrections for PF MET is AK4PFchs jets with JES corrected pT > 15 GeV (using the L1L2L3-L1 scheme).
        # The jets that are used to correct MET are also required to have electromagnetic energy fraction smaller than 0.9 and not to be overlapping with the pf muon candidate'
        jets_met_t1_mask = (
            (jets_L123.pt > 15)
            & (self.events.Jet.neEmEF + self.events.Jet.chEmEF < 0.9)
            & delta_r_mask(self.events.Jet, self.events.Muon, 0.4)
        )
        jets_L123 = jets_L123[jets_met_t1_mask]
        jets_L1 = jets_L1[jets_met_t1_mask]
        # get correction factor components
        corr_factor_px = ak.sum((jets_L123 - jets_L1).px, axis=1)
        corr_factor_py = ak.sum((jets_L123 - jets_L1).py, axis=1)
        # get corrected MET components
        met_px = self.events.MET.pt * np.cos(self.events.MET.phi) - corr_factor_px
        met_py = self.events.MET.pt * np.sin(self.events.MET.phi) - corr_factor_py
        # update nominal MET
        self.events["MET", "pt"] = np.sqrt((met_px**2.0 + met_py**2.0))
        self.events["MET", "phi"] = np.arctan2(met_py, met_px)

    def apply_met_jer_corr(self):
        corrected_met_pt, corrected_met_phi = corrected_polar_met(
            met_pt=self.events.MET.pt,
            met_phi=self.events.MET.phi,
            other_phi=self.events.Jet.phi,
            other_pt_old=self.events.Jet.pt_jec,
            other_pt_new=self.events.Jet.pt_jer,
        )
        # update nominal MET
        self.events["MET", "pt"] = corrected_met_pt
        self.events["MET", "phi"] = corrected_met_phi

    def apply_met_unclustered_energy_corr(self):
        """
        corrected_met_pt_up, corrected_met_phi_up = corrected_polar_met(
            met_pt=self.events.MET.pt,
            met_phi=self.events.MET.phi,
            other_phi=self.events.Jet.phi,
            other_pt_old=self.events.Jet.pt_raw,
            other_pt_new=self.events.Jet.pt,
            dx=self.events.MET.MetUnclustEnUpDeltaX,
            dy=self.events.MET.MetUnclustEnUpDeltaY,
            positive=True
        )
        # update nominal MET
        self.events["MET", "pt"] = corrected_met_pt
        self.events["MET", "phi"] = corrected_met_phi
        """
        pass
