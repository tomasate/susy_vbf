from analysis.configs.dataset_config import DatasetConfig


dataset_config = DatasetConfig(name = "QCD_Pt-20To30_EMEnriched",
                               process= "QCD",
                               query= "QCD_Pt-20to30_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL16NanoAODv9-106X_mcRun2_asymptotic_v17-v2/NANOAODSIM",
                               year= "2016",
                               is_mc= "True"
                               xsec= 5352960.0,
                               partitions= {'nsplit': 2})