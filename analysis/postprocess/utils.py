import os
import pickle
import logging

def setup_logger(output_dir):
    """Set up the logger to log to a file in the specified output directory."""
    output_file_path = os.path.join(output_dir, "postprocess_logs.txt")
    logging.basicConfig(
        level=logging.INFO,
        format="%(message)s",
        handlers=[logging.FileHandler(output_file_path), logging.StreamHandler()],
    )

def open_output(fname: str) -> dict:
    with open(fname, "rb") as f:
        output = pickle.load(f)
    return output

def print_header(text):
    logging.info("-" * 90)
    logging.info(text)
    logging.info("-" * 90)