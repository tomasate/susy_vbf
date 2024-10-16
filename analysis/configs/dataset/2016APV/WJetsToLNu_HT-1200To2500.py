from analysis.configs.dataset_config import DatasetConfig


dataset_config = DatasetConfig(name = "WJetsToLNu_HT-1200To2500",
                               process= "WJetsToLNu",
                               query= "WJetsToLNu_HT-1200To2500_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL16NanoAODAPVv9-106X_mcRun2_asymptotic_preVFP_v11-v1/NANOAODSIM",
                               year= "2016APV",
                               is_mc= "True"
                               xsec= 1.074,
                               partitions= {'nsplit': 3})