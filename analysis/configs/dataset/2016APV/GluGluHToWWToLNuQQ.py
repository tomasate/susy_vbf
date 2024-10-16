from analysis.configs.dataset_config import DatasetConfig


dataset_config = DatasetConfig(name = "GluGluHToWWToLNuQQ",
                               process= "Higgs",
                               query= "GluGluHToWWToLNuQQ_M-125_TuneCP5_13TeV_powheg_jhugen751_pythia8/RunIISummer20UL16NanoAODAPVv9-106X_mcRun2_asymptotic_preVFP_v11-v1/NANOAODSIM",
                               year= "2016APV",
                               is_mc= "True"
                               xsec= 28.88,
                               partitions= {'nsplit': 1})