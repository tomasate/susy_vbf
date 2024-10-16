from analysis.configs.dataset_config import DatasetConfig


dataset_config = DatasetConfig(
    name="ST_t-channel_antitop_4f_InclusiveDecays",
    process="SingleTop",
    query="ST_t-channel_antitop_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v1/NANOAODSIM",
    year="2017",
    is_mc="True",
    xsec=71.74,
    partitions=5,
)
