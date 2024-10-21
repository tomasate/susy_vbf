from analysis.configs.dataset_config import DatasetConfig


dataset_config = DatasetConfig(
    name="TTToHadronic",
    process="tt",
    query="TTToHadronic_TuneCP5CR1_13TeV-powheg-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v2/NANOAODSIM",
    year="2018",
    is_mc="True",
    xsec=377.96,
    partitions=12,
)
