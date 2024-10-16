from analysis.configs.dataset_config import DatasetConfig


dataset_config = DatasetConfig(name = "DYJetsToLL_M-4to50_HT-400to600",
                               process= "DYJetsToLL",
                               query= "DYJetsToLL_M-4to50_HT-400to600_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL16NanoAODv9-106X_mcRun2_asymptotic_v17-v2/NANOAODSIM",
                               year= "2016",
                               is_mc= "True"
                               xsec= 3.581,
                               partitions= {'nsplit': 5})