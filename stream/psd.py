#!/bin/python3


from scipy import signal
import numpy as np
import matplotlib.pyplot as plt
import argparse
import acq400_hapi
import concurrent.futures
import sys
from itertools import repeat


def get_args():
    parser = argparse.ArgumentParser(description='Power spectral density')

    parser.add_argument('--file', default="./afhba.0.log", type=str,
    help='Which data file to analyse')

    parser.add_argument('uut', nargs=1, help="uut ")
    args = parser.parse_args()
    return args


def perform_psd(channel, fs):

    # Calculate the periodogram.
    f, Pxx_den = signal.periodogram(channel, window='hanning')

    # Normalise so we don't go over 0dB.
    Pxx_den = Pxx_den / np.max(Pxx_den)

    # Take the log so we can view it properly.
    Pxx_den = 10*np.log10(Pxx_den)
    return [f, Pxx_den]


def main():

    args = get_args()

#    uut = acq400_hapi.Acq400(args.uut[0])
#    print("1")
#    nchan = uut.get_ai_channels()
#    print("2")
#    fs = round(float(uut.s0.SIG_CLK_MB_FREQ.split(" ")[1]))
#    print("3")
#    _dtype = np.int32 if int(uut.s0.data32) else np.int16

    nchan = 128
    fs = 20000
    _dtype = np.int16

    while True:
        data = []
        # read in 1M samples from stdin
        print("Reading data now")
        rawdata = sys.stdin.buffer.read(int(1e5 * nchan))
        print("Read data")
        rawdata = np.fromstring(rawdata, dtype=_dtype)

        for ch in range(0, 1):
            data.append(np.array(rawdata[ch::nchan]))

        data[0] = data[0] / 32768 * 10

        with concurrent.futures.ThreadPoolExecutor() as executor:
            # Here we will get a thread per channel.
            results = executor.map(perform_psd, data, repeat(fs))
            for result in results:
                print(result[0], result[1])
                plt.plot(result[0], result[1])
            #plt.plot(data[0])
            plt.xlabel('frequency [Hz]')
            plt.ylabel('Normalised PSD (dB)')
            plt.show()



if __name__ == '__main__':
    main()

