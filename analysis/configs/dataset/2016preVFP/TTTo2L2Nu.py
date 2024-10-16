from analysis.configs.dataset_config import DatasetConfig


dataset_config = DatasetConfig(
    name="TTTo2L2Nu",
    process="tt",
    query="TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16NanoAODAPVv9-106X_mcRun2_asymptotic_preVFP_v11-v1/NANOAODSIM",
    year="2016preVFP",
    is_mc="True",
    xsec=88.29,
    partitions=8,
)
