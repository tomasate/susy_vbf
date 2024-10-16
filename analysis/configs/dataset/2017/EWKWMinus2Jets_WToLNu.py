from analysis.configs.dataset_config import DatasetConfig


dataset_config = DatasetConfig(name = "EWKWMinus2Jets_WToLNu",
                               process= "EWK",
                               query= "EWKWMinus2Jets_WToLNu_M-50_TuneCP5_withDipoleRecoil_13TeV-madgraph-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v2/NANOAODSIM",
                               year= "2017",
                               is_mc= "True"
                               xsec= 20.35,
                               partitions= {'nsplit': 2})