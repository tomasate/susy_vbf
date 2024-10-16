from analysis.configs.dataset_config import DatasetConfig


dataset_config = DatasetConfig(name = "DYJetsToLL_M-4to50_HT-70to100",
                               process= "DYJetsToLL",
                               query= "DYJetsToLL_M-4to50_HT-70to100_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v3/NANOAODSIM",
                               year= "2018",
                               is_mc= "True"
                               xsec= None,
                               partitions= {'nsplit': 3})