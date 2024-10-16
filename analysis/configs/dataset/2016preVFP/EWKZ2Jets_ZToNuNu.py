from analysis.configs.dataset_config import DatasetConfig


dataset_config = DatasetConfig(
    name="EWKZ2Jets_ZToNuNu",
    process="EWK",
    query="EWKZ2Jets_ZToNuNu_M-50_TuneCP5_withDipoleRecoil_13TeV-madgraph-pythia8/RunIISummer20UL16NanoAODAPVv9-106X_mcRun2_asymptotic_preVFP_v11-v2/NANOAODSIM",
    year="2016preVFP",
    is_mc="True",
    xsec=10.04,
    partitions=3,
)
