from analysis.configs.dataset_config import DatasetConfig


dataset_config = DatasetConfig(name = "WJetsToLNu_inclusive",
                               process= "WJetsToLNu",
                               query= "WJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL16NanoAODAPVv9-106X_mcRun2_asymptotic_preVFP_v11-v2/NANOAODSIM",
                               year= "2016APV",
                               is_mc= "True"
                               xsec= 61334.0,
                               partitions= {'nsplit': 9})