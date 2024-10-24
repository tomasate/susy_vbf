import os
import json
import argparse
from pathlib import Path
from coffea.dataset_tools.dataset_query import DataDiscoveryCLI


ERAS = {
    "2016preVFP": ["B1", "B2", "C", "D", "E", "F"],
    "2016postVFP": ["F", "G", "H"],
    "2017": ["B", "C", "D", "E", "F"],
    "2018": ["A", "B", "C", "D"],
}

SITES = {
    "2016preVFP": [
        "T3_US_FNALLPC",
        "T1_US_FNAL_Disk",
        "T2_US_Vanderbilt",
        "T2_US_Purdue",
        "T2_US_Nebraska",
        "T2_DE_DESY",
        "T2_BE_IIHE",
        "T2_CH_CERN",
        "T1_DE_KIT_Disk",
        "T2_DE_RWTH",
        "T2_BE_UCL",
        "T1_UK_RAL_Disk",
        "T1_FR_CCIN2P3_Disk"
        "T2_RU_JINR",
        "T2_UK_London_IC",
        "T1_FR_CCIN2P3_Disk"
    ],
    "2016postVFP": [
        "T3_US_FNALLPC",
        "T1_US_FNAL_Disk",
        "T2_US_Vanderbilt",
        "T2_US_Purdue",
        "T2_US_Nebraska",
        "T2_DE_DESY",
        "T2_BE_IIHE",
        "T2_CH_CERN",
        "T1_DE_KIT_Disk",
        "T2_DE_RWTH",
        "T2_BE_UCL",
        "T1_UK_RAL_Disk",
        "T1_FR_CCIN2P3_Disk"
        "T2_RU_JINR",
        "T2_UK_London_IC",
        "T1_FR_CCIN2P3_Disk"
    ],
    "2017": [
        "T3_US_FNALLPC",
        "T1_US_FNAL_Disk",
        "T2_US_Vanderbilt",
        "T2_US_Purdue",
        "T2_US_Nebraska",
        "T2_DE_DESY",
        "T2_BE_IIHE",
        "T2_CH_CERN",
        "T1_DE_KIT_Disk",
        "T2_DE_RWTH",
        "T2_BE_UCL",
        "T1_UK_RAL_Disk",
        "T1_FR_CCIN2P3_Disk"
        "T2_RU_JINR",
        "T2_UK_London_IC",
        "T1_FR_CCIN2P3_Disk",
        "T3_CH_PSI",
        "T3_CH_PSI",
        "T2_ES_CIEMAT"
    ],
    "2018": [
        "T3_US_FNALLPC",
        "T1_US_FNAL_Disk",
        "T2_US_Vanderbilt",
        "T2_US_Purdue",
        "T2_US_Nebraska",
        "T2_DE_DESY",
        "T2_BE_IIHE",
        "T2_CH_CERN",
        "T1_DE_KIT_Disk",
        "T2_DE_RWTH",
        "T2_BE_UCL",
        "T1_UK_RAL_Disk",
        "T1_FR_CCIN2P3_Disk"
        "T2_RU_JINR",
        "T2_UK_London_IC",
        "T1_FR_CCIN2P3_Disk",
        "T2_EE_Estonia"
    ],
}

def main(args):
    # open dataset configs
    with open(f"{Path.cwd()}/{args.year}_datasets.json", "r") as f:
        dataset_configs = json.load(f)
    # read dataset queries
    das_queries = {}
    for sample in dataset_configs:
        das_queries[sample] = dataset_configs[sample]["query"]
    
    for year in ERAS.keys():
        if args.year != "all":
            if year != args.year:
                continue
        # create a dataset_definition dict for each yeare
        dataset_definition = {}
        for dataset_key, query in das_queries.items():
            if isinstance(query, list):
                for _query, era in zip(query, ERAS[year]):
                    dataset_definition[f"/{_query}"] = {
                        "short_name": f"{dataset_key}_{era}",
                        "metadata": {"isMC": False},
                    }
            else:
                dataset_definition[f"/{query}"] = {
                    "short_name": dataset_key,
                    "metadata": {"isMC": True},
                }
        # the dataset definition is passed to a DataDiscoveryCLI
        ddc = DataDiscoveryCLI()
        # set the allow sites to look for replicas
        ddc.do_allowlist_sites(SITES[year])
        # query rucio and get replicas
        ddc.load_dataset_definition(
            dataset_definition,
            query_results_strategy="all",
            replicas_strategy="round-robin",
        )
        ddc.do_save(f"dataset_discovery_{args.year}.json")

        # load and reformat generated fileset
        with open(f"dataset_discovery_{args.year}.json", "r") as f:
            dataset_discovery = json.load(f)
        new_dataset = {key: [] for key in das_queries}
        for dataset in dataset_discovery:
            root_files = list(dataset_discovery[dataset]["files"].keys())
            dataset_key = dataset_discovery[dataset]["metadata"]["short_name"]
            if dataset_key.startswith("Single"):
                new_dataset[dataset_key.split("_")[0]] += root_files
            else:
                new_dataset[dataset_key] = root_files
        # save new fileset and drop 'dataset_discovery' fileset
        os.remove(f"dataset_discovery_{args.year}.json")
        with open(f"fileset_{args.year}_NANO_lxplus.json", "w") as json_file:
            json.dump(new_dataset, json_file, indent=4, sort_keys=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--year",
        dest="year",
        type=str,
        default="2017",
        help="year of the data {2016preVFP, 2016postVFP, 2017, 2018}",
    )
    args = parser.parse_args()
    main(args)