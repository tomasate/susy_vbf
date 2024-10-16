from analysis.configs.dataset_config import DatasetConfig


dataset_config = DatasetConfig(name = "QCD_Pt-120To170_EMEnriched",
                               process= "QCD",
                               query= "QCD_Pt-120to170_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL16NanoAODv9-106X_mcRun2_asymptotic_v17-v2/NANOAODSIM",
                               year= "2016",
                               is_mc= "True"
                               xsec= 629664.0,
                               partitions= {'nsplit': 2})