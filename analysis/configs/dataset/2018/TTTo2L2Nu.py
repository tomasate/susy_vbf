from analysis.configs.dataset_config import DatasetConfig


dataset_config = DatasetConfig(
    name="TTTo2L2Nu",
    process="tt",
    query="TTTo2L2Nu_TuneCP5CR1_13TeV-powheg-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v2/NANOAODSIM",
    year="2018",
    is_mc="True",
    xsec=88.29,
    partitions=8,
)
