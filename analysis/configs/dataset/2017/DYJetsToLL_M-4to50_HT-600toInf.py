from analysis.configs.dataset_config import DatasetConfig


dataset_config = DatasetConfig(
    name="DYJetsToLL_M-4to50_HT-600toInf",
    process="DYJetsToLL",
    query="DYJetsToLL_M-4to50_HT-600toInf_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v3/NANOAODSIM",
    year="2017",
    is_mc="True",
    xsec=1.124,
    partitions=3,
)
