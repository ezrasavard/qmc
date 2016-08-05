#!/usr/bin/python

import numpy as np
import math
import matplotlib.pyplot as plt 
import sys

from scipy.optimize import curve_fit

def func(x, a, b, c, d):

    return a*((x+b)**c) + d

def xfunc(x, N, a, b):

    return x

def yfunc(y, N, a, b):

    return y

if __name__ == "__main__":

    plist = []
    plist.append(["MAJ", "../results/dists_maj/diffs.npy",  'r', 's', 14])
    plist.append(["Split2", "../results/split2/diffs.npy",  'm', '>', 27])
    plist.append(["Split3", "../results/split3/diffs.npy",  'c', '<', 42])
    plist.append(["Wire", "../results/wire50_20/diffs.npy",  'y', '*', 50])
    plist.append(["INV", "../results/dists_inv/diffs.npy",  'g', 'x', 52])
    plist.append(["XOR", "../results/dists_xor/diffs.npy", 'b', 'o', 102])
    plist.append(["MEM", "../results/dists_mem/diffs.npy", 'k', 'v', 215])
    outfile = "../results/diffs_comparison.png"
    block_size = 40

    try:
        diff_percentage = float(sys.argv[1])
    except:
        diff_percentage = 20 

    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    all_x = []
    all_y = []

    for row in plist:
        data = np.load(row[1])
        # throw away low PTxJ and MCSxS noise
        data = data[data[:,0] > 8]
        data = data[data[:,1] > 14]
        z = data[:,2]
        diff_thresh = np.percentile(z, diff_percentage)
        data = data[data[:,2] <= diff_thresh]
        N = row[4]
        x = xfunc(data[:,0], N, 1, .35)
        y = yfunc(data[:,1], N, 1, .65)

        label = "{}, N={}".format(row[0],row[4])
        ax1.scatter(x, y, s=block_size, alpha=0.5, label=label, c=row[2], marker=row[3])
        popt, pcov = curve_fit(func, x, y, maxfev=100000)
        print("Problem: {}, N: {}".format(row[0],row[4]))
        print("\t{:.2f}*((x + {:.2f})**{:.2f}) + {:.2f}".format(*popt))
        plt.plot(x, func(x, *popt), c=row[2])
        all_x += list(x)
        all_y += list(y)

    popt, pcov = curve_fit(func, all_x, all_y, maxfev=100000)
    all_x = np.sort(all_x)
    plt.plot(all_x, func(all_x, *popt), c='k', linewidth=10, alpha=0.5)
    regstring = "{:.2f}*((x + {:.2f})**{:.2f}) + {:.2f}".format(*popt)
    print("Best Fit:\n\t{}".format(regstring))
    plt.xlabel("PTxJ")
    plt.ylabel("MCSxS")
#     plt.yscale('log')
    plt.legend(loc='upper left')
    plt.title("Lowest {:.0f}% of Distribution Difference".format(diff_percentage))
    plt.show()
