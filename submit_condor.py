import json
import argparse
from pathlib import Path
from condor import submit_condor
from analysis.fileset import divide_list
from analysis.helpers.path_handler import Paths


def get_output_directories(args: dict) -> str:
    """builds output directories for data and metadata. Return output path"""
    # get processor output path
    paths = Paths(eval(args["eos"]))
    processor_output_path = paths.processor_path(
        processor_name=args["processor"],
        dataset_year=args["year"],
        label=args["label"],
        mkdir=True,
    )
    return str(processor_output_path)


def main(args):
    args = vars(args)
    submit = eval(args["submit"])
    args["output_path"] = get_output_directories(args)
    del args["label"]
    del args["eos"]
    del args["submit"]

    # split dataset into batches
    fileset_path = Path(f"{Path.cwd()}/analysis/fileset")
    with open(f"{fileset_path}/fileset_{args['year']}_NANO_lxplus.json", "r") as f:
        root_files = json.load(f)[args["dataset"]]
    root_files_list = divide_list(root_files)

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
        help="processor to be used {ztojets}",
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
        help="whether to include underflow/overflow to first/last bin {True, False}",
    )
    parser.add_argument(
        "--submit",
        dest="submit",
        type=str,
        default="True",
        help="if True submit job to Condor. If False, it just builds datasets and condor files",
    )
    parser.add_argument(
        "--label",
        dest="label",
        type=str,
        default="ZJets_CR",
        help="Tag to recognize the run",
    )
    parser.add_argument(
        "--eos",
        dest="eos",
        type=str,
        default="True",
        help="if True save outputs to /eos",
    )
    args = parser.parse_args()
    main(args)
