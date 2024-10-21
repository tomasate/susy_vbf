from analysis.configs.dataset_config import DatasetConfig


dataset_config = DatasetConfig(
    name="ST_s-channel_4f_leptonDecays",
    process="SingleTop",
    query="ST_s-channel_4f_leptonDecays_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL16NanoAODv9-106X_mcRun2_asymptotic_v17-v1/NANOAODSIM",
    year="2016postVFP",
    is_mc="True",
    xsec=3.549,
    partitions=2,
)
