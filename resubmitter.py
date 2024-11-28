import json
import glob
import yaml
import argparse
import subprocess
from pathlib import Path


def main(args):
    """Helper function to resubmit condor jobs"""

    main_dir = Path.cwd()

    # get outputs path
    out_path = f"{args.output_path}/{args.processor}/{args.label}/{args.year}"
    print(f"Reading outputs from: {out_path}")

    # get datasets
    fileset_path = Path(f"{main_dir}/analysis/filesets")
    with open(f"{fileset_path}/{args.year}_fileset.yaml", "r") as f:
        datasets = yaml.safe_load(f)

    # get jobs done
    jobs_done = []
    for sample in datasets:
        output_list = glob.glob(f"{out_path}/{sample}*.pkl")
        for output in output_list:
            jobs_done.append(output.split("/")[-1].replace(".pkl", ""))
    n_jobs_done = len(jobs_done)

    # get jobs to be run
    condor_path = main_dir / "condor" / args.processor / args.label / args.year
    condor_files = glob.glob(f"{condor_path}/*/*.sub", recursive=True)
    n_jobs = len(condor_files)

    # get jobs names
    condor_files_keys = [
        f.split("/")[-1].replace(f"{args.processor}_", "").replace(".sub", "")
        for f in condor_files
    ]

    for job, sub_file in zip(condor_files_keys, condor_files):
        if job not in jobs_done:
            print(job)
            if args.resubmit == "True":
                # resubmit missing jobs
                subprocess.run(["condor_submit", sub_file])

    print("")
    print(f"{n_jobs=}")
    print(f"{n_jobs_done=}")
    print(f"missing files: {n_jobs - n_jobs_done}", "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output_path",
        dest="output_path",
        type=str,
        # default="/eos/user/t/tatehort/susy_vbf/outs"
        help="path to the 'outs' folder",
    )
    parser.add_argument(
        "--label",
        dest="label",
        type=str,
        default="",
        help="label of the run",
    )
    parser.add_argument(
        "--processor",
        dest="processor",
        type=str,
        default="ztojets",
        help="processor to be used",
    )
    parser.add_argument(
        "--year",
        dest="year",
        type=str,
        default="2017",
        help="year of the data {2016preVFP, 2016postVFP, 2017, 2018} (default 2017)",
    )
    parser.add_argument(
        "--resubmit",
        dest="resubmit",
        type=str,
        default="False",
        help="if True resubmit the jobs. if False only print the missing jobs",
    )
    args = parser.parse_args()
    main(args)
