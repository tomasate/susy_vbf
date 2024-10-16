from analysis.configs.dataset_config import DatasetConfig


dataset_config = DatasetConfig(name = "TTToHadronic",
                               process= "tt",
                               query= "TTToHadronic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16NanoAODAPVv9-106X_mcRun2_asymptotic_preVFP_v11-v1/NANOAODSIM",
                               year= "2016APV",
                               is_mc= "True"
                               xsec= 377.96,
                               partitions= {'nsplit': 12})