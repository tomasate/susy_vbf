from analysis.configs.dataset_config import DatasetConfig


dataset_config = DatasetConfig(
    name="WZ",
    process="Diboson",
    query="WZ_TuneCP5_13TeV-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v1/NANOAODSIM",
    year="2017",
    is_mc="True",
    xsec=27.59,
    partitions=2,
)
