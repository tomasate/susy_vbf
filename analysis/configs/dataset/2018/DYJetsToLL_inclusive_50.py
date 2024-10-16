from analysis.configs.dataset_config import DatasetConfig


dataset_config = DatasetConfig(name = "DYJetsToLL_inclusive_50",
                               process= "DYJetsToLL",
                               query= "DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM",
                               year= "2018",
                               is_mc= "True"
                               xsec= 6025.6,
                               partitions= {'nsplit': 8})