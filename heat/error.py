"""Computes the error between FDM and IDRLnet solutions

To compare the differences in both methods, we compute the deviation between
solutions provided via FDM and via IDRLnet. This error (absolute value of the
difference) is computed for each spatio-temporal point.
Finally, this error is plotted in a figure with the error for each timeframe or
in an animated file (gif).
"""

import os

from absl import app
from absl import logging
from absl import flags

import pickle

import utils.plot

FLAGS = flags.FLAGS

# Directories
flags.DEFINE_string(
    "fdm_folder", "fdm_results",
    "Folder where the results of the desired FDM run are stored.")
flags.DEFINE_string("idrlnet_folder", "idrlnet_run",
                    "Folder where the desired idrlnet model is stored.")
flags.DEFINE_list(
    "output_format", ["figure", "gif"], "Defines the formats in which the "
    "output is obtained. Only two formats are available: gif and figure. "
    "If 'figure' is in the list provided, it outputs a figure with several "
    "subplots at different timesteps. If 'gif' is in the list provided, it "
    "outputs a gif with several plots at different timesteps.")


def main(_):

    current_directory = os.getcwd()

    # Load FDM results
    fdm_directory = os.path.join(current_directory, FLAGS.fdm_folder)
    with open(os.path.join(fdm_directory, "fdm_results.pickle"), "rb") as f:
        fdm_memorized_timeframes = pickle.load(f)

    # Load IDRLnet results and metadata
    idrlnet_directory = os.path.join(current_directory, FLAGS.idrlnet_folder)
    with open(os.path.join(idrlnet_directory, "results", "data.pickle"),
              "rb") as f:
        idrlnet_memorized_timeframes, metadata = pickle.load(f)

    # Comparison between FDM and IDRLnet solutions (each instant at a time)
    error_timeframes = []
    for fdm_instant_solution, idrlnet_instant_solution in zip(
            fdm_memorized_timeframes, idrlnet_memorized_timeframes):
        time = fdm_instant_solution[0]
        abs_error = abs(fdm_instant_solution[1] - idrlnet_instant_solution[1])
        error_timeframes.append([time, abs_error])

    # Error directory
    error_directory = os.path.join(idrlnet_directory, "error_results")
    if not os.path.exists(error_directory):
        os.mkdir(error_directory)

    # Plot results
    if "figure" in FLAGS.output_format:
        utils.plot.generate_figures_across_time(
            error_timeframes,
            metadata["plate_length"],
            metadata["diff_coef"],
            metadata["holes_list"],
            metadata["holes_temp"],
            error_directory,
            error_bool=True,
        )
    if "gif" in FLAGS.output_format:
        utils.plot.generate_gif_across_time(
            error_timeframes,
            metadata["plate_length"],
            metadata["diff_coef"],
            metadata["holes_list"],
            metadata["holes_temp"],
            error_directory,
            error_bool=True,
        )


if __name__ == "__main__":
    logging.set_verbosity(logging.INFO)
    app.run(main)
