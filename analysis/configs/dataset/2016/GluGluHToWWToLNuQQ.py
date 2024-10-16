from analysis.configs.dataset_config import DatasetConfig


dataset_config = DatasetConfig(name = "GluGluHToWWToLNuQQ",
                               process= "Higgs",
                               query= "GluGluHToWWToLNuQQ_M-125_TuneCP5_13TeV_powheg_jhugen751_pythia8/RunIISummer20UL16NanoAODv9-106X_mcRun2_asymptotic_v17-v1/NANOAODSIM",
                               year= "2016",
                               is_mc= "True"
                               xsec= 28.88,
                               partitions= {'nsplit': 1})