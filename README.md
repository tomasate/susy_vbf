# susy_vbf

#### How to submit jobs

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
cd analysis/fileset/

# run the 'make_filesets' script
python make_filesets.py --year <year>

# exit the singularity
exit
```

Jobs are submitted via the `submit_condor.py` script:
```bash
usage: submit_condor.py [-h] [--processor PROCESSOR] [--dataset DATASET] [--year YEAR] [--flow FLOW] [--submit SUBMIT] [--label LABEL] [--eos]

options:
  -h, --help            show this help message and exit
  --processor PROCESSOR
                        processor to be used (default ztojets)
  --dataset DATASET     sample key to be processed
  --year YEAR           year of the data {2016preVFP, 2016postVFP, 2017, 2018} (default 2017)
  --flow FLOW           whether to include underflow/overflow to first/last bin {True, False} (default True)
  --submit SUBMIT       if True submit job to Condor. If False, it just builds datasets and condor files (default True)
  --label LABEL         Tag to label the run (default ztojets_CR)
  --eos                 Enable saving outputs to /eos
```
Example:
```
python3 submit_condor.py --processor ztojets --dataset <sample> --year 2017 --label test --eos
```
Outputs will be save to `/eos/user/<username first letter>/<username>/susy_vbf/outs/<processor>/<label>/<year>`


#### Postprocessing

Once you have run the corresponding datasets for the processor, you can get the results using the `run_run_postprocess.py` script:
```bash
usage: run_postprocess.py [-h] [--processor PROCESSOR] [--year YEAR] [--label LABEL] [--eos] [--output_dir OUTPUT_DIR] [--log_scale]

optional arguments:
  -h, --help            show this help message and exit
  --processor PROCESSOR
                        processor to be used {ztojets}
  --year YEAR           year of the data {2016preVFP, 2016postVFP, 2017, 2018} (default 2017)
  --label LABEL         Label of the output directory
  --eos                 Enable reading outputs from /eos
  --output_dir OUTPUT_DIR
                        Path to the outputs directory
  --log_scale           Enable log scale for y-axis
```
Example:
```bash
singularity shell -B /cvmfs -B /pnfs -B /user /cvmfs/unpacked.cern.ch/registry.hub.docker.com/coffeateam/coffea-base-almalinux8:0.7.22-py3.8

python3 run_postprocess.py --processor ztojets --year 2017 --label test --eos
``` 
You can also add the `--log_scale` flag to change the y-axis to log scale. Results will be saved to the same directory as the output files