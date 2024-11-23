import json
import yaml
import argparse
from pathlib import Path
from condor import submit_condor
from analysis.filesets import divide_list
from analysis.helpers import get_output_directory


def main(args):
    args = vars(args)
    submit = eval(args["submit"])
    args["output_path"] = get_output_directory(args)
    del args["label"]
    del args["eos"]
    del args["submit"]

    # split dataset into batches
    fileset_path = Path(f"{Path.cwd()}/analysis/filesets")
    with open(f"{fileset_path}/fileset_{args['year']}_NANO_lxplus.json", "r") as f:
        root_files = json.load(f)[args["dataset"]]
    root_files_list = divide_list(root_files, args["nfiles"])
    del args["nfiles"]

    # submit job for each partition
    for i, partition in enumerate(root_files_list, start=1):
        if len(root_files_list) == 1:
            args["dataset_key"] = args["dataset"]
            args["partition_fileset"] = {args["dataset"]: partition}
        else:
            args["nsample"] = i
            dataset_key = f'{args["dataset"]}_{i}'
            args["dataset_key"] = dataset_key
            args["partition_fileset"] = {dataset_key: partition}
        submit_condor(args, submit=submit)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--processor",
        dest="processor",
        type=str,
        default="ztojets",
        help="processor to be used (default ztojets)",
    )
    parser.add_argument(
        "--dataset",
        dest="dataset",
        type=str,
        default="",
        help="sample key to be processed",
    )
    parser.add_argument(
        "--year",
        dest="year",
        type=str,
        default="2017",
        help="year of the data {2016preVFP, 2016postVFP, 2017, 2018} (default 2017)",
    )
    parser.add_argument(
        "--flow",
        dest="flow",
        type=str,
        default="True",
        help="whether to include underflow/overflow to first/last bin {True, False} (default True)",
    )
    parser.add_argument(
        "--submit",
        dest="submit",
        type=str,
        default="True",
        help="if True submit job to Condor. If False, it just builds datasets and condor files (default True)",
    )
    parser.add_argument(
        "--label",
        dest="label",
        type=str,
        default="ztojets_CR",
        help="Tag to label the run (default ztojets_CR)",
    )
    parser.add_argument(
        "--eos",
        action="store_true",
        help="Enable saving outputs to /eos",
    )
    parser.add_argument(
        "--nfiles",
        dest="nfiles",
        type=int,
        default=20,
        help="number of root files to include in each dataset partition (default 20)",
    )
    args = parser.parse_args()
    main(args)
