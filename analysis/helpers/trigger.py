import awkward as ak

def trigger_match(leptons: ak.Array, trigobjs: ak.Array, trigger_path: str):
    """
    Returns DeltaR matched trigger objects 
    
    leptons:
        electrons or muons arrays
    trigobjs:
        trigger objects array
    trigger_path:
        trigger to match {IsoMu27, Ele35_WPTight_Gsf}
        
    https://twiki.cern.ch/twiki/bin/viewauth/CMS/EgammaNanoAOD#Trigger_bits_how_to
    """
    match_configs = {
        "IsoMu27": {
            "pt": trigobjs.pt > 25,
            "filterbit": (trigobjs.filterBits & 8) > 0,
            "id": abs(trigobjs.id) == 13
        },
        "Ele35_WPTight_Gsf": {
            "pt": trigobjs.pt > 33,
            "filterbit": (trigobjs.filterBits & 2) > 0,
            "id": abs(trigobjs.id) == 11
        }
    }
    pass_pt = match_configs[trigger_path]["pt"]
    pass_id = match_configs[trigger_path]["id"]
    pass_filterbit = match_configs[trigger_path]["filterbit"]
    trigger_cands = trigobjs[pass_pt & pass_id & pass_filterbit]
    delta_r = leptons.metric_table(trigger_cands)
    pass_delta_r = delta_r < 0.1
    n_of_trigger_matches = ak.sum(pass_delta_r, axis=2)
    trig_matched_locs = n_of_trigger_matches >= 1
    return trig_matched_locs