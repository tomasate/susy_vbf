from analysis.configs.dataset_config import DatasetConfig


dataset_config = DatasetConfig(name = "EWKZ2Jets_ZToNuNu",
                               process= "EWK",
                               query= "EWKZ2Jets_ZToNuNu_M-50_TuneCP5_withDipoleRecoil_13TeV-madgraph-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v2/NANOAODSIM",
                               year= "2018",
                               is_mc= "True"
                               xsec= 10.04,
                               partitions= {'nsplit': 3})