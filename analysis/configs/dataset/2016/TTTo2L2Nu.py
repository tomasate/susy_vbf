from analysis.configs.dataset_config import DatasetConfig


dataset_config = DatasetConfig(name = "TTTo2L2Nu",
                               process= "tt",
                               query= "TTTo2L2Nu_TuneCP5CR1_13TeV-powheg-pythia8/RunIISummer20UL16NanoAODv9-106X_mcRun2_asymptotic_v17-v1/NANOAODSIM",
                               year= "2016",
                               is_mc= "True"
                               xsec= 88.29,
                               partitions= {'nsplit': 8})