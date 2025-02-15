# SUSY VBF

Python package for analyzing compressed mass spectrum SUSY via electroweak VBF with 0-, 1-, and 2-lepton final states. The package uses a columnar framework to process input tree-based NanoAODv12 files using [Coffea](https://coffeateam.github.io/coffea/) and [scikit-hep](https://scikit-hep.org) Python libraries.

- [Processors](#Processors)
- [Generate input datasets](#Generate-input-datasets)
- [Submit Condor jobs](#Submit-Condor-jobs)
- [Postprocessing](#Postprocessing)


### Processors

* `ztojets`: Select events for a Z+jets 0-lepton channel

The processors are defined in [`analysis/processors/<processor>.py`](https://github.com/deoache/susy_vbf/tree/main/analysis/processors). The selections, variables, output histograms, triggers, among other features, are defined through a configuration file located in `analysis/configs/processor/<processor>/<year>.yaml` (see [here](https://github.com/deoache/susy_vbf/blob/main/analysis/configs/README.md) for a detailed description). 

### Generate input datasets

Connect to lxplus and clone the repository (if you have not done it yet)
```
# connect to lxplus 
ssh <your_username>@lxplus.cern.ch

# clone the repository 
git clone https://github.com/deoache/susy_vbf.git
cd susy_vbf
```
You need to have a valid grid proxy in the CMS VO. (see [here](https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideLcgAccess) for details on how to register in the CMS VO). The needed grid proxy is obtained via the usual command
```
voms-proxy-init --voms cms
```
Use the [make_filesets.py](https://github.com/deoache/susy_vbf/blob/main/analysis/fileset/make_filesets.py) script to build the input filesets with xrootd endpoints:
```
# get the singularity shell 
singularity shell -B /afs -B /eos -B /cvmfs /cvmfs/unpacked.cern.ch/registry.hub.docker.com/coffeateam/coffea-dask:latest-py3.10

# move to the fileset directory
cd analysis/filesets/

# run the 'make_filesets' script
python make_filesets.py --year <year>

# exit the singularity
exit
```
### Submit Condor jobs
Jobs are submitted via the `submit_condor.py` script:
```bash
usage: submit_condor.py [-h] [--processor PROCESSOR] [--dataset DATASET] [--year YEAR] [--flow FLOW] [--submit] [--label LABEL] [--eos] [--nfiles NFILES]
                        [--do_systematics]

optional arguments:
  -h, --help            show this help message and exit
  --processor PROCESSOR
                        processor to be used (default ztojets)
  --dataset DATASET     sample key to be processed
  --year YEAR           year of the data {2016preVFP, 2016postVFP, 2017, 2018} (default 2017)
  --flow FLOW           whether to include underflow/overflow to first/last bin {True, False} (default True)
  --submit              Enable Condor job submission. If not provided, it just builds condor files
  --label LABEL         Tag to label the run (default ztojets_CR)
  --eos                 Enable saving outputs to /eos
  --nfiles NFILES       number of root files to include in each dataset partition (default 20)
  --do_systematics      Enable applying systematics
```
Example:
```
python3 submit_condor.py --processor ztojets --dataset <sample> --year 2017 --label test --eos
```
**Note**: It's recommended to add the `--eos` flag so that the outputs are save in your `/eos` area, so that postprocessing can be done from [SWAN](https://swan-k8s.cern.ch/hub/spawn). **In this case, you will need to clone the repo also in SWAN before submitting jobs in order to be able to run the postprocess step afterwards**.

The [runner.py](https://github.com/deoache/susy_vbf/blob/main/runner.py) script is built on top of `submit_condor.py` and can be used to submit all jobs (MC + Data) for certain processor/year
```
usage: runner.py [-h] [--processor PROCESSOR] [--year YEAR] [--nfiles NFILES] [--label LABEL] [--submit] [--eos] [--do_systematics]

optional arguments:
  -h, --help            show this help message and exit
  --processor PROCESSOR
                        processor to be used {ztojets} (default ztojets)
  --year YEAR           dataset year {2016preVFP, 2016postVFP, 2017, 2018} (default 2017)
  --nfiles NFILES       number of root files to include in each dataset partition (default 20)
  --label LABEL         Tag to label the run (default ztojets_CR)
  --submit              Enable Condor job submission. If not provided, it just builds condor files
  --eos                 Enable saving outputs to /eos
  --do_systematics      Enable applying systematics
```
Example:
```
python3 runner.py --processor ztojets --year 2017 --label test --submit --eos 
``` 
After submitting the jobs you can watch their status by typing:
```
watch condor_q
```
You can use the `resubmitter.py` script to see which jobs have not yet been completed
```
usage: resubmitter.py [-h] [--processor PROCESSOR] [--year YEAR] [--label LABEL] [--resubmit] [--eos]

optional arguments:
  -h, --help            show this help message and exit
  --processor PROCESSOR
                        processor to be used
  --year YEAR           year of the data {2016preVFP, 2016postVFP, 2017, 2018} (default 2017)
  --label LABEL         label of the run
  --resubmit            if True resubmit the jobs. if False only print the missing jobs
  --eos                 Enable reading outputs from /eos
```
Example:
```
python3 resubmitter.py --processor ztojets --year 2017 --label test --eos 
```
Some jobs might crash due to some site being down. In this case, identify and remove the problematic site from the [sites list](https://github.com/deoache/higgscharm/blob/lxplus/analysis/filesets/make_filesets.py#L9-L31), generate the datasets again with `make_filesets.py`, create new condor files with `runner.py` or `submit_condor.py` (without the `--submit` flag), and resubmit the missing jobs adding the `--resubmit` flag:
```
python3 resubmitter.py --processor ztojets --year 2017 --label test --eos --resubmit
```

### Postprocessing

Once you have run the corresponding datasets for the processor, you can get the results using the `run_postprocess.py` script:
```bash
usage: run_postprocess.py [-h] [--processor PROCESSOR] [--year YEAR] [--label LABEL] [--eos] [--log_scale] [--yratio_limits YRATIO_LIMITS YRATIO_LIMITS]
                          [--output_dir OUTPUT_DIR] [--savefig] [--extension EXTENSION]

optional arguments:
  -h, --help            show this help message and exit
  --processor PROCESSOR
                        processor to be used {ztojets}
  --year YEAR           year of the data {2016preVFP, 2016postVFP, 2017, 2018} (default 2017)
  --label LABEL         Label of the output directory
  --eos                 Enable reading outputs from /eos
  --log_scale           Enable log scale for y-axis
  --yratio_limits YRATIO_LIMITS YRATIO_LIMITS
                        Set y-axis ratio limits as a tuple (e.g., --yratio_limits 0.5 1.5) (default 0 2)
  --output_dir OUTPUT_DIR
                        Path to the outputs directory (optional)
  --savefig             Enable plot saving
  --extension EXTENSION
                        extension to be used for plotting {png, pdf}
```
Example:
```
# from the susy_vbf folder in SWAN (105a release)
python3 run_postprocess.py --processor ztojets --year 2017 --label test --eos --log_scale --savefig
``` 
Results will be saved to the same directory as the output files