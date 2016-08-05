#!/usr/bin/python

import dwave
import numpy as np
import matplotlib.pyplot as plt
import string
import sys

if __name__ == "__main__":

    fname = sys.argv[1]
    data = []
    with open(fname) as fp:
        for i, line in enumerate(fp):
            if i == 0:
                continue
            data.append(line)
            if i == 3e6: # I don't want to run out of RAM
                break

    data = np.array([string.split(x) for x in data], dtype=np.float32)

    
    print(data)
    print(data.shape)
    bins = np.linspace(0, 9000, 100)
    f, axarr = plt.subplots(2, sharex=True)
    axarr[0].scatter(data[:,0], data[:,1], s=2, alpha=0.1, color='blue')
    axarr[0].set_title('An attempt at plotting spectra from QMC')
    for E in np.unique(data[:,1]):
        tmp = data[(data[:,1] == E), 0]
#         print(tmp)
#         h, b = np.histogram(tmp, bins)
#         plt.plot(b[:-1], h)
#         plt.show()
        axarr[1].hist(tmp, bins, histtype='step', normed=False, label=str(E))
#         break
    plt.yscale('symlog', linthreshy=10000)
    plt.legend(loc='best')
    plt.xlabel('Tau')
    plt.ylabel('State energy (including neighbour coupling)')

    plt.show()

