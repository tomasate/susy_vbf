from analysis.configs.dataset_config import DatasetConfig


dataset_config = DatasetConfig(
    name="WW",
    process="Diboson",
    query="WW_TuneCP5_13TeV-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM",
    year="2018",
    is_mc="True",
    xsec=75.95,
    partitions=2,
)
