from analysis.configs.dataset_config import DatasetConfig


dataset_config = DatasetConfig(name = "QCD_HT1500to2000",
                               process= "QCD",
                               query= "QCD_HT1500to2000_TuneCP5_PSWeights_13TeV-madgraph-pythia8/RunIISummer20UL16NanoAODAPVv9-106X_mcRun2_asymptotic_preVFP_v11-v1/NANOAODSIM",
                               year= "2016APV",
                               is_mc= "True"
                               xsec= 101.0,
                               partitions= {'nsplit': 3})