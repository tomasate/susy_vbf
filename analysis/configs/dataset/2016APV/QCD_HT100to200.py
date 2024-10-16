from analysis.configs.dataset_config import DatasetConfig


dataset_config = DatasetConfig(name = "QCD_HT100to200",
                               process= "QCD",
                               query= "QCD_HT100to200_TuneCP5_PSWeights_13TeV-madgraph-pythia8/RunIISummer20UL16NanoAODAPVv9-106X_mcRun2_asymptotic_preVFP_v11-v1/NANOAODSIM",
                               year= "2016APV",
                               is_mc= "True"
                               xsec= 27990000.0,
                               partitions= {'nsplit': 4})