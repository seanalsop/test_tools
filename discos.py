#!/usr/bin/env python


"""discos.py checks a stream of data for discontinuities.
It then compares the positions of the discos to
positions of the mux pattern changes in the
SPAD.
"""


import argparse
import numpy as np
import sys


def run_disco_check(args):
    # Check data for discontinuities.
    change_flag = False
    while True:
        data = sys.stdin.read(args.read_kbytes*1024)
        data = np.fromstring(data, dtype=np.int32)

        ch = data[args.ch::104]
        mux_changing = data[args.chans + 2::104]
        sample_counts = data[args.chans + 0::104]
        mux_pattern = data[args.chans + 3::104]

        for index, item in enumerate(ch):
            #print sample_counts[index], mux_changing[index], mux_pattern[index]
            if index == 0:
                continue
            if item - ch[index - 1] > args.disco_size:
                #print "Disco found at index: ", index
                # print item - ch[index - 1]
                for place, val in enumerate(mux_pattern[index - 100 : index + 100]):
                    if place == 0:
                        prev = val
                        continue
                    if val != prev:
                        #print "Mux has changed alongside mux change indicator."
                        change_flag = True
                        # if place < 500 or place > 1500:
                            # print "Larger than expected gap between disco and mux pattern: ", place
                        break
                    prev = val

                if not change_flag:
                    print "ILLEGAL DISCONTINUITY FOUND."
                    print "disco: ", item - ch[index - 1]
                    print "index: ", index
                    print "place = ", place
                    print "val, prev:", val, prev
                    print "change_flag: ", change_flag

                    ch.tofile("ch1.dat")
                    mux_pattern.tofile("mux_pattern.dat")
                else:
                    change_flag = False

    return None


def run_main():
    parser = argparse.ArgumentParser(description="Mux pattern test")

    parser.add_argument('--chans', default=24*4, type=int,
    help='Number of channels as longs.')

    parser.add_argument('--ch', default=0, type=int,
    help='Which channel to inspect for discontinuities.')

    parser.add_argument('--read_kbytes', default=41600, type=int,
    help='How many megabytes to read at once from STDIN.')

    parser.add_argument('--disco_size', default=11000000*3, type=int,
    help='Control the minimum size of discontinuities that will flag.')

    run_disco_check(parser.parse_args())


if __name__ == '__main__':
    run_main()
