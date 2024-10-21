from analysis.configs.dataset_config import DatasetConfig


dataset_config = DatasetConfig(
    name="ST_t-channel_antitop_4f_InclusiveDecays",
    process="SingleTop",
    query="ST_t-channel_antitop_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM",
    year="2018",
    is_mc="True",
    xsec=71.74,
    partitions=5,
)
