from analysis.configs.dataset_config import DatasetConfig


dataset_config = DatasetConfig(name = "TTToHadronic",
                               process= "tt",
                               query= "TTToHadronic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v1/NANOAODSIM",
                               year= "2017",
                               is_mc= "True"
                               xsec= 377.96,
                               partitions= {'nsplit': 12})