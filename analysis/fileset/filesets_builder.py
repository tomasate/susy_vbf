import glob
import json
from pathlib import Path


def build_fileset_partitions(sample_name: str, year: str) -> dict:
    """
    builds partition filesets from a single fileset

    Parameters:
        sample_name:
            name of the dataset
        year:
            year of the dataset {2016preVFP, 2016postVFP, 2017, 2018}
    """
    # get fileset path
    fileset_path = Path(f"{Path.cwd()}/analysis/fileset")

    # make processed fileset directory
    output_directory = Path(f"{fileset_path}/{year}")
    if output_directory.exists():
        for file in output_directory.glob(f"{sample_name}*"):
            if file.is_file():
                file.unlink()
    else:
        output_directory.mkdir(parents=True)

    # get fileset root files
    with open(f"{fileset_path}/fileset_{year}_NANO_lxplus.json", "r") as f:
        root_files = json.load(f)[sample_name]

    # split fileset and save partitions
    root_files_list = divide_list(root_files)
    if len(root_files_list) == 1:
        partition_fileset = {sample_name: root_files_list}
        with open(f"{output_directory}/{sample_name}.json", "w") as json_file:
            json.dump(partition_fileset, json_file, indent=4, sort_keys=True)
    else:
        for i, partition in enumerate(root_files_list, start=1):
            key = f"{sample_name}_{i}"
            with open(f"{output_directory}/{key}.json", "w") as json_file:
                json.dump({key: partition}, json_file, indent=4, sort_keys=True)


def divide_list(lst: list) -> list:
    """Divide a list into sublists such that each sublist has at least 20 elements."""
    if len(lst) < 20:
        return [lst]

    # Dynamically calculate the number of sublists such that each has at least 20 elements
    n = len(lst) // 20  # This gives the number of groups with at least 20 elements
    if len(lst) % 20 != 0:
        n += 1  # Increase n by 1 if there is a remainder, to accommodate extra elements

    # Divide the list into 'n' sublists
    size = len(lst) // n
    remainder = len(lst) % n
    result = []
    start = 0

    for i in range(n):
        if i < remainder:
            end = start + size + 1
        else:
            end = start + size
        result.append(lst[start:end])
        start = end

    return result