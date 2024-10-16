from analysis.configs.dataset_config import DatasetConfig


dataset_config = DatasetConfig(
    name="DYJetsToLL_M-50_HT-2500toInf",
    process="DYJetsToLL",
    query="DYJetsToLL_M-50_HT-2500toInf_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8/RunIISummer20UL16NanoAODv9-106X_mcRun2_asymptotic_v17-v2/NANOAODSIM",
    year="2016postVFP",
    is_mc="True",
    xsec=0.003514,
    partitions=2,
)
