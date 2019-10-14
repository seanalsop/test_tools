#!/bin/python3


from scipy import signal
import numpy as np
import matplotlib.pyplot as plt
import argparse
import acq400_hapi
import concurrent.futures


def get_args():
    parser = argparse.ArgumentParser(description='Power spectral density')

    parser.add_argument('--file', default="./afhba.0.log", type=str,
    help='Which data file to analyse')

    parser.add_argument('uut', nargs=1, help="uut ")
    args = parser.parse_args()
    return args


def perform_psd(channel, fs):
    f, Pxx_den = signal.welch(channel, fs)
    return [f, Pxx_den]


def main():

    args = get_args()

    uut = acq400_hapi.Acq400(args.uut[0])
    nchan = uut.get_ai_channels()
    fs = round(float(uut.s0.SIG_CLK_MB_FREQ.split(" ")[1]))
    _dtype = np.int32 if int(uut.s0.data32) else np.int16

    # Calculate the power spectral density
    # rawdata = np.fromfile(args.file, dtype=_dtype)

    while True:
        data = []
        # read in 1M samples from stdin
        rawdata = sys.stdin.read(1e6 * nchan)
        rawdata = np.fromstring(data, dtype=_dtype)
        for ch in range(0, nchan):
            data.append(np.array(rawdata[ch::nchan]))


        with concurrent.futures.ThreadPoolExecutor() as executor:
            # Here we will get a thread per channel.
            results = executor.map(perform_psd, data, fs)
            for result in results:
                plt.semilogy(result[0], result[1])
            plt.xlabel('frequency [Hz]')
            plt.ylabel('PSD [V**2/Hz]')
            plt.show()



if __name__ == '__main__':
    main()

