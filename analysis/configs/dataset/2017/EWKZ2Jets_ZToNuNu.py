from analysis.configs.dataset_config import DatasetConfig


dataset_config = DatasetConfig(
    name="EWKZ2Jets_ZToNuNu",
    process="EWK",
    query="EWKZ2Jets_ZToNuNu_M-50_TuneCP5_withDipoleRecoil_13TeV-madgraph-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v2/NANOAODSIM",
    year="2017",
    is_mc="True",
    xsec=10.04,
    partitions=3,
)
