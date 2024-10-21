from analysis.configs.dataset_config import DatasetConfig


dataset_config = DatasetConfig(
    name="Tau",
    process="Data",
    query="['Tau/Run2016F-UL2016_MiniAODv2_NanoAODv9-v1/NANOAOD', 'Tau/Run2016G-UL2016_MiniAODv2_NanoAODv9-v1/NANOAOD', 'Tau/Run2016H-UL2016_MiniAODv2_NanoAODv9-v1/NANOAOD']",
    year="2016postVFP",
    is_mc="False",
    xsec=None,
    partitions=15,
)
