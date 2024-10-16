from analysis.configs.dataset_config import DatasetConfig


dataset_config = DatasetConfig(name = "DYJetsToLL_M-50_HT-200to400",
                               process= "DYJetsToLL",
                               query= "DYJetsToLL_M-50_HT-200to400_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM",
                               year= "2018",
                               is_mc= "True"
                               xsec= 48.63,
                               partitions= {'nsplit': 4})