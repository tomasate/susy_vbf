from analysis.configs.dataset_config import DatasetConfig


dataset_config = DatasetConfig(
    name="WW",
    process="Diboson",
    query="WW_TuneCP5_13TeV-pythia8/RunIISummer20UL16NanoAODv9-106X_mcRun2_asymptotic_v17-v1/NANOAODSIM",
    year="2016postVFP",
    is_mc="True",
    xsec=75.95,
    partitions=2,
)
