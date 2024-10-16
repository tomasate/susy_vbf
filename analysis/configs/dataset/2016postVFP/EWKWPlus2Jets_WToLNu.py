from analysis.configs.dataset_config import DatasetConfig


dataset_config = DatasetConfig(
    name="EWKWPlus2Jets_WToLNu",
    process="EWK",
    query="EWKWPlus2Jets_WToLNu_M-50_TuneCP5_withDipoleRecoil_13TeV-madgraph-pythia8/RunIISummer20UL16NanoAODv9-106X_mcRun2_asymptotic_v17-v1/NANOAODSIM",
    year="2016postVFP",
    is_mc="True",
    xsec=25.81,
    partitions=3,
)
