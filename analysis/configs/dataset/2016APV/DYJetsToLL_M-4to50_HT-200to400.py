from analysis.configs.dataset_config import DatasetConfig


dataset_config = DatasetConfig(name = "DYJetsToLL_M-4to50_HT-200to400",
                               process= "DYJetsToLL",
                               query= "DYJetsToLL_M-4to50_HT-200to400_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL16NanoAODAPVv9-106X_mcRun2_asymptotic_preVFP_v11-v2/NANOAODSIM",
                               year= "2016APV",
                               is_mc= "True"
                               xsec= 37.2,
                               partitions= {'nsplit': 3})