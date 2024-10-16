from analysis.configs.dataset_config import DatasetConfig


dataset_config = DatasetConfig(
    name="TTToHadronic",
    process="tt",
    query="TTToHadronic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16NanoAODv9-106X_mcRun2_asymptotic_v17-v1/NANOAODSIM",
    year="2016postVFP",
    is_mc="True",
    xsec=377.96,
    partitions=12,
)
