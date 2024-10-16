from analysis.configs.dataset_config import DatasetConfig


dataset_config = DatasetConfig(
    name="MET",
    process="Data",
    query="['MET/Run2016B-ver1_HIPM_UL2016_MiniAODv2_NanoAODv9-v2/NANOAOD', 'MET/Run2016B-ver2_HIPM_UL2016_MiniAODv2_NanoAODv9-v2/NANOAOD', 'MET/Run2016C-HIPM_UL2016_MiniAODv2_NanoAODv9-v2/NANOAOD', 'MET/Run2016D-HIPM_UL2016_MiniAODv2_NanoAODv9-v2/NANOAOD', 'MET/Run2016E-HIPM_UL2016_MiniAODv2_NanoAODv9-v2/NANOAOD', 'MET/Run2016F-HIPM_UL2016_MiniAODv2_NanoAODv9-v2/NANOAOD']",
    year="2016preVFP",
    is_mc="False",
    xsec=None,
    partitions=15,
)
