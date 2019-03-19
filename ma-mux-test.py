#!/usr/bin/env python


"""
A script to analyse the mux pattern of stored data. Mux pattern is stored in the
spad.
"""

import argparse
import struct
import sys
import numpy as np
import matplotlib.pyplot as plt


def run_analysis(args):
    diffs = []
    #change_indexes = []
    while True:
        change_indexes = []
        # data = np.fromfile(args.file, dtype=np.int32) # load data as longs
        data = sys.stdin.read(args.read_mbytes*1024**2)
        # data = np.frombuffer(data)
        data = np.fromstring(data, dtype=np.int32)


        # Pull out the points of interest from the spad.
        mux_changing = data[args.chans + 2::104]
        sample_counts = data[args.chans + 0::104]
        mux_pattern = data[args.chans + 3::104]

        for index, item in enumerate(mux_pattern):
            if index == 0:
                continue
            if item != mux_pattern[index - 1]:
                change_indexes.append(index)

        for num, item in enumerate(change_indexes):
            if num == 0:
                continue
            # print "Sample difference = ", item - change_indexes[num-1]
            diffs.append(item - change_indexes[num-1])
            if item - change_indexes[num-1] < 0:
                print "item, index_num = ", item, change_indexes[num-1]

        # Print each point in a column
        # for num, item in enumerate(sample_counts):
        #     print "{:>8} {:>8} {:>8}".format(sample_counts[num], \
        #     mux_changing[num], mux_pattern[num])
        # for num, item in enumerate(diffs):
        #     print num, item
        if args.plot == 1:
            # plt.plot(sample_counts, mux_pattern)
            plt.clf()
            n, bins, patches = plt.hist(diffs, bins=30)
            # plt.show()
            plt.pause(0.1)

    return None


def run_main():
    parser = argparse.ArgumentParser(description="Mux pattern test")

    parser.add_argument('--chans', default=24*4, type=int,
    help='Number of channels as longs.')

    parser.add_argument('--file', default='acq2106_112_data', type=str,
    help='File to analyse.')

    parser.add_argument('--plot', default=0, type=int,
    help='Whether or not to plot the sample count vs mux pattern.')

    parser.add_argument('--read_mbytes', default=416, type=int,
    help='How many megabytes to read at once from STDIN.')

    run_analysis(parser.parse_args())


if __name__ == '__main__':
    run_main()