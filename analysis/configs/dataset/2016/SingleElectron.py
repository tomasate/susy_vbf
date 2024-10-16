from analysis.configs.dataset_config import DatasetConfig


dataset_config = DatasetConfig(name = "SingleElectron",
                               process= "Data",
                               query= "['SingleElectron/Run2016F-UL2016_MiniAODv2_NanoAODv9-v1/NANOAOD', 'SingleElectron/Run2016G-UL2016_MiniAODv2_NanoAODv9-v1/NANOAOD', 'SingleElectron/Run2016H-UL2016_MiniAODv2_NanoAODv9-v1/NANOAOD']",
                               year= "2016",
                               is_mc= "False"
                               xsec= None,
                               partitions= {'nsplit': 15})