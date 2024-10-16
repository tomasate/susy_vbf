from analysis.configs.dataset_config import DatasetConfig


dataset_config = DatasetConfig(name = "EWKZ2Jets_ZToLL",
                               process= "EWK",
                               query= "EWKZ2Jets_ZToLL_M-50_TuneCP5_withDipoleRecoil_13TeV-madgraph-pythia8/RunIISummer20UL16NanoAODv9-106X_mcRun2_asymptotic_v17-v1/NANOAODSIM",
                               year= "2016",
                               is_mc= "True"
                               xsec= 3.997,
                               partitions= {'nsplit': 2})