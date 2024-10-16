from analysis.configs.dataset_config import DatasetConfig


dataset_config = DatasetConfig(name = "DYJetsToLL_inclusive_10to50",
                               process= "DYJetsToLL",
                               query= "DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL16NanoAODv9-106X_mcRun2_asymptotic_v17-v1/NANOAODSIM",
                               year= "2016",
                               is_mc= "True"
                               xsec= 18610.0,
                               partitions= {'nsplit': 8})