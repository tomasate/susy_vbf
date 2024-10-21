from analysis.configs.dataset_config import DatasetConfig


dataset_config = DatasetConfig(
    name="WW",
    process="Diboson",
    query="WW_TuneCP5_13TeV-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v1/NANOAODSIM",
    year="2017",
    is_mc="True",
    xsec=75.95,
    partitions=2,
)
