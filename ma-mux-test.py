#!/usr/bin/env python


"""
A script to analyse the mux pattern of stored data. Mux pattern is stored in the
spad.
"""

import argparse
import numpy as np
import matplotlib.pyplot as plt


def run_analysis(args):
    data = np.fromfile(args.file, dtype=np.int32) # load data as longs

    # Pull out the points of interest from the spad.
    mux_changing = data[args.chans + 2::104]
    sample_counts = data[args.chans + 0::104]
    mux_pattern = data[args.chans + 3::104]

    # Print each point in a column
    for num, item in enumerate(sample_counts):
        print "{:>8} {:>8} {:>8}".format(sample_counts[num], \
        mux_changing[num], mux_pattern[num])

    # if args.print == 1:
    #     plt.plot(sample_counts, mux_pattern)
    #     plt.show()

    return None


def run_main():
    parser = argparse.ArgumentParser(description="Mux pattern test")
    parser.add_argument('--chans', default=24*4, type=int,
    help='Number of channels as longs.')
    parser.add_argument('--file', default='acq2106_112_data', type=str,
    help='File to analyse.')
    parser.add_argument('--plot', default=0, type=int,
    help='Whether or not to plot the sample count vs mux pattern.')
    run_analysis(parser.parse_args())


if __name__ == '__main__':
    run_main()