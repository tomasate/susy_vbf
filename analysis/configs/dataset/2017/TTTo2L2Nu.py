from analysis.configs.dataset_config import DatasetConfig


dataset_config = DatasetConfig(name = "TTTo2L2Nu",
                               process= "tt",
                               query= "TTTo2L2Nu_TuneCP5CR1_13TeV-powheg-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v2/NANOAODSIM",
                               year= "2017",
                               is_mc= "True"
                               xsec= 88.29,
                               partitions= {'nsplit': 8})