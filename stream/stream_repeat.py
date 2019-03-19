#!/usr/bin/env python

"""
stream_repeat.py is a script that initiates a stream and pulls an arbitrary
amount of data from port 4210. The data can be verified using the sample
counter between runs.
"""

import acq400_hapi
import argparse
import numpy as np
import socket
import sys
# import matplotlib.pyplot as plt
import time


def verify_spad(args, data):
    # Check whether each successive sample counter gets incremented by 1.
    for iter, sample_count in data[96::104]:
        if iter == 0: # first iteration
            val = sample_count
        else:
            if sample_count != val + 1:
                return False # return false if the sample counter jumps.
            else:
                val = sample_count
                continue
    return True # return true if all of the sample counters are sequential.


def run_test(args):

    # Setup
    uut = acq400_hapi.Acq400(args.uuts[0])
    uut.s1.trg = "1,1,1" # use soft trigger
    skt = socket.socket()

    rxbuf_len = 4096
    data = ""
    counter = 1
    args.nchan = int(uut.s0.NCHAN) if args.nchan == -1 else args.nchan
    print args.nchan
    while counter < args.loops:

        print "Starting loop: ", counter
        # Start stream
        skt = socket.socket()
        skt.connect((args.uuts[0], 4210))
        while sys.getsizeof(data) < (1024**2): # pull 1MB
            data += skt.recv(rxbuf_len)
        skt.close()
        # Get numpy array from string data
        data = np.frombuffer(bytes(data), dtype=args.data_type)

        if args.verify == 1:
            verify_spad(args, data)

        # plt.plot(data[0::args.nchan])
        # plt.show()
        data = ""
        print "Successfully finished loop: ", counter
        counter += 1
        time.sleep(1)


    return None


def run_main():
    parser = argparse.ArgumentParser(description='Repeated stream test')

    parser.add_argument('--loops', default=sys.maxint, type=int,
    help="Number of test iterations to run.")

    parser.add_argument('--verify', default=1, type=int,
    help="Whether to verify the sample counter.")

    parser.add_argument('--data_type', default=np.int32, type=int,
    help="Data type of the data to being streamed.")

    parser.add_argument('--nchan', default=-1, type=int,
    help="Number of channels the system has. Default: query system.")

    parser.add_argument('uuts', nargs='+', help="uuts")
    run_test(parser.parse_args())


if __name__ == '__main__':
    run_main()