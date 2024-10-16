from analysis.configs.dataset_config import DatasetConfig


dataset_config = DatasetConfig(name = "ST_tW_antitop_5f_inclusiveDecays",
                               process= "SingleTop",
                               query= "ST_tW_antitop_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16NanoAODAPVv9-106X_mcRun2_asymptotic_preVFP_v11-v1/NANOAODSIM",
                               year= "2016APV",
                               is_mc= "True"
                               xsec= 34.97,
                               partitions= {'nsplit': 3})