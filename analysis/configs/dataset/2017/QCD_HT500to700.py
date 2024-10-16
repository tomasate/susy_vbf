from analysis.configs.dataset_config import DatasetConfig


dataset_config = DatasetConfig(name = "QCD_HT500to700",
                               process= "QCD",
                               query= "QCD_HT500to700_TuneCP5_PSWeights_13TeV-madgraph-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v1/NANOAODSIM",
                               year= "2017",
                               is_mc= "True"
                               xsec= 29070.0,
                               partitions= {'nsplit': 4})