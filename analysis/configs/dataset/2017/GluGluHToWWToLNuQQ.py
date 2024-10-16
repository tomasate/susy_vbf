from analysis.configs.dataset_config import DatasetConfig


dataset_config = DatasetConfig(name = "GluGluHToWWToLNuQQ",
                               process= "Higgs",
                               query= "GluGluHToWWToLNuQQ_M-125_TuneCP5_13TeV_powheg_jhugen751_pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v1/NANOAODSIM",
                               year= "2017",
                               is_mc= "True"
                               xsec= 28.88,
                               partitions= {'nsplit': 1})