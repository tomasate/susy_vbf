from analysis.configs.dataset_config import DatasetConfig


dataset_config = DatasetConfig(
    name="ST_tW_top_5f_inclusiveDecays",
    process="SingleTop",
    query="ST_tW_top_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v2/NANOAODSIM",
    year="2018",
    is_mc="True",
    xsec=34.91,
    partitions=3,
)
