from analysis.configs.dataset_config import DatasetConfig


dataset_config = DatasetConfig(name = "QCD_Pt-800To1000_MuEnriched",
                               process= "QCD",
                               query= "QCD_Pt-800To1000_MuEnrichedPt5_TuneCP5_13TeV-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v2/NANOAODSIM",
                               year= "2017",
                               is_mc= "True"
                               xsec= 4.7,
                               partitions= {'nsplit': 11})