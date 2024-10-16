from analysis.configs.dataset_config import DatasetConfig


dataset_config = DatasetConfig(name = "ST_tW_top_5f_inclusiveDecays",
                               process= "SingleTop",
                               query= "ST_tW_top_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16NanoAODv9-106X_mcRun2_asymptotic_v17-v2/NANOAODSIM",
                               year= "2016",
                               is_mc= "True"
                               xsec= 34.91,
                               partitions= {'nsplit': 3})