from analysis.configs.dataset_config import DatasetConfig


dataset_config = DatasetConfig(name = "Tau",
                               process= "Data",
                               query= "['Tau/Run2018A-UL2018_MiniAODv2_NanoAODv9-v2/NANOAOD', 'Tau/Run2018B-UL2018_MiniAODv2_NanoAODv9-v1/NANOAOD', 'Tau/Run2018C-UL2018_MiniAODv2_NanoAODv9-v1/NANOAOD', 'Tau/Run2018D-UL2018_MiniAODv2_NanoAODv9-v2/NANOAOD']",
                               year= "2018",
                               is_mc= "False"
                               xsec= None,
                               partitions= {'nsplit': 15})