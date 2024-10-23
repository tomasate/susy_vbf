import awkward as ak
from analysis.helpers.path_handler import Paths


def delta_r_mask(first: ak.Array, second: ak.Array, threshold: float) -> ak.Array:
    """
    Select objects from 'first' which are at least threshold away from all objects in 'second'.
    The result is a mask (i.e., a boolean array) of the same shape as first.
    
    Parameters:
    -----------
    first: 
        objects which are required to be at least threshold away from all objects in second
    second: 
        objects which are all objects in first must be at leats threshold away from
    threshold: 
        minimum delta R between objects

    Return:
    -------
        boolean array of objects in objects1 which pass delta_R requirement
    """
    mval = first.metric_table(second)
    return ak.all(mval > threshold, axis=-1)


def get_output_directory(args: dict) -> str:
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