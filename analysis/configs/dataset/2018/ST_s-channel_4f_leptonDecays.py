from analysis.configs.dataset_config import DatasetConfig


dataset_config = DatasetConfig(name = "ST_s-channel_4f_leptonDecays",
                               process= "SingleTop",
                               query= "ST_s-channel_4f_leptonDecays_TuneCP5CR1_13TeV-amcatnlo-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v2/NANOAODSIM",
                               year= "2018",
                               is_mc= "True"
                               xsec= 3.549,
                               partitions= {'nsplit': 2})