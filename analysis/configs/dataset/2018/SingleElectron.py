from analysis.configs.dataset_config import DatasetConfig


dataset_config = DatasetConfig(
    name="SingleElectron",
    process="Data",
    query="['EGamma/Run2018A-UL2018_MiniAODv2_NanoAODv9-v1/NANOAOD', 'EGamma/Run2018B-UL2018_MiniAODv2_NanoAODv9-v1/NANOAOD', 'EGamma/Run2018C-UL2018_MiniAODv2_NanoAODv9-v1/NANOAOD', 'EGamma/Run2018D-UL2018_MiniAODv2_NanoAODv9-v3/NANOAOD']",
    year="2018",
    is_mc="False",
    xsec=None,
    partitions=15,
)
