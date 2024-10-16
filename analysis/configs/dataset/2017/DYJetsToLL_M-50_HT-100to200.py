from analysis.configs.dataset_config import DatasetConfig


dataset_config = DatasetConfig(name = "DYJetsToLL_M-50_HT-100to200",
                               process= "DYJetsToLL",
                               query= "DYJetsToLL_M-50_HT-100to200_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v1/NANOAODSIM",
                               year= "2017",
                               is_mc= "True"
                               xsec= 160.7,
                               partitions= {'nsplit': 3})