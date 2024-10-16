from analysis.configs.dataset_config import DatasetConfig


dataset_config = DatasetConfig(name = "ST_t-channel_top_4f_InclusiveDecays",
                               process= "SingleTop",
                               query= "ST_t-channel_top_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8/RunIISummer20UL16NanoAODAPVv9-106X_mcRun2_asymptotic_preVFP_v11-v1/NANOAODSIM",
                               year= "2016APV",
                               is_mc= "True"
                               xsec= 119.7,
                               partitions= {'nsplit': 8})