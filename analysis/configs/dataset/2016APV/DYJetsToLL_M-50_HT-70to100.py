from analysis.configs.dataset_config import DatasetConfig


dataset_config = DatasetConfig(name = "DYJetsToLL_M-50_HT-70to100",
                               process= "DYJetsToLL",
                               query= "DYJetsToLL_M-50_HT-70to100_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8/RunIISummer20UL16NanoAODAPVv9-106X_mcRun2_asymptotic_preVFP_v11-v2/NANOAODSIM",
                               year= "2016APV",
                               is_mc= "True"
                               xsec= 140.0,
                               partitions= {'nsplit': 2})