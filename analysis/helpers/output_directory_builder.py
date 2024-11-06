from analysis.helpers.path_handler import Paths

def get_output_directory(args: dict) -> str:
    """builds output directories for data and metadata. Return output path"""
    # get processor output path
    paths = Paths(eos=args["eos"])
    processor_output_path = paths.processor_path(
        processor_name=args["processor"],
        dataset_year=args["year"],
        label=args["label"],
        mkdir=True,
    )
    return str(processor_output_path)