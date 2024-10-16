from analysis.configs.dataset_config import DatasetConfig


dataset_config = DatasetConfig(name = "WJetsToLNu_HT-2500ToInf",
                               process= "WJetsToLNu",
                               query= "WJetsToLNu_HT-2500ToInf_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL16NanoAODv9-106X_mcRun2_asymptotic_v17-v2/NANOAODSIM",
                               year= "2016",
                               is_mc= "True"
                               xsec= 0.008001,
                               partitions= {'nsplit': 2})