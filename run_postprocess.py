import os
import glob
import yaml
import logging
import argparse
from analysis.helpers import get_output_directory
from analysis.configs import ProcessorConfigBuilder
from analysis.postprocess.plotter import Plotter
from analysis.postprocess.postprocessor import Postprocessor
from analysis.postprocess.utils import print_header, setup_logger


def clear_output_directory(output_dir):
    """Delete all result files in the output directory."""
    extensions = ["*.csv", "*.txt", "*.png", "*.pdf"]
    for ext in extensions:
        files = glob.glob(os.path.join(output_dir, ext))
        for file in files:
            os.remove(file)

def plot(args, processed_histograms, histograms_config, lumi, cat_axis=None):
    plotter = Plotter(
        processor=args.processor,
        processed_histograms=processed_histograms,
        year=args.year,
        lumi=lumi,
        cat_axis=cat_axis,
        output_dir=args.output_dir,
    )
    print_header("plotting histograms")
    if histograms_config.layout == "individual":
        for feature in histograms_config.axes:
            logging.info(feature)
            plotter.plot_feature_hist(
                feature=feature,
                feature_label=histograms_config.axes[feature]["label"],
                yratio_limits=(0, 2),
                divide_by_bin_width=histograms_config.axes[feature]["type"] == "Variable",
                log_scale=args.log_scale,
                savefig=True,
            )
    else:
        for key, features in histograms_config.layout.items():
            for feature in features:
                logging.info(feature)
                plotter.plot_feature_hist(
                    feature=feature,
                    feature_label=histograms_config.axes[feature]["label"],
                    yratio_limits=(0, 2),
                    divide_by_bin_width=histograms_config.axes[feature]["type"] == "Variable",
                    log_scale=args.log_scale,
                    savefig=True,
                )

def main(args):
    if not args.output_dir:
        args.output_dir = get_output_directory(vars(args))
        
    # delete previous results
    clear_output_directory(args.output_dir)

    # set up logger
    setup_logger(args.output_dir)

    # save processor config
    config_builder = ProcessorConfigBuilder(processor=args.processor, year=args.year)
    processor_config = config_builder.build_processor_config()
    logging.info(processor_config.to_yaml())

    # process (group and accumulate) outputs
    postprocessor = Postprocessor(
        processor=args.processor,
        year=args.year,
        output_dir=args.output_dir,
    )
    processed_histograms = postprocessor.histograms
    lumi = postprocessor.luminosities[args.year]

    # plot histograms
    histograms_config = processor_config.histogram_config
    if histograms_config.add_cat_axis:
        for k in histograms_config.add_cat_axis:
            categories = histograms_config.add_cat_axis[k]["categories"] + [sum]
            for category in categories:
                logging.info(f"plotting {category} category of {k} axis")
                plot(args, processed_histograms, histograms_config, lumi, (k, category))
    else:
        plot(args, processed_histograms, histograms_config, lumi, None)


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
        "--year",
        dest="year",
        type=str,
        default="2017",
        help="year of the data {2017}",
    )
    parser.add_argument(
        "--label",
        dest="label",
        type=str,
        help="Label of the output directory",
    )
    parser.add_argument(
        "--eos",
        action="store_true",
        help="Enable reading outputs from /eos",
    )
    parser.add_argument(
        "--output_dir",
        dest="output_dir",
        type=str,
        help="Path to the outputs directory",
    )
    parser.add_argument(
        "--log_scale",
        action="store_true",
        help="Enable log scale for y-axis",
    )
    args = parser.parse_args()
    main(args)