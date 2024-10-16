from analysis.configs.dataset_config import DatasetConfig


dataset_config = DatasetConfig(name = "QCD_HT500to700",
                               process= "QCD",
                               query= "QCD_HT500to700_TuneCP5_PSWeights_13TeV-madgraph-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM",
                               year= "2018",
                               is_mc= "True"
                               xsec= 29070.0,
                               partitions= {'nsplit': 4})