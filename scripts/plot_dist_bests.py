#!/usr/bin/python

import numpy as np
import matplotlib.pyplot as plt 
import sys

if __name__ == "__main__":

    plist = []
    plist.append(["MAJ, N=14", "../results/dists_maj/diffs.npy",  'r', 's'])
    plist.append(["Wire, N=50", "../results/wire50_20/diffs.npy",  'y', '*'])
    plist.append(["Split2, N=27", "../results/split2/diffs.npy",  'm', '>'])
    plist.append(["Split3, N=42", "../results/split3/diffs.npy",  'c', '<'])
    plist.append(["INV, N=52", "../results/dists_inv/diffs.npy",  'g', 'x'])
    plist.append(["XOR, N=102", "../results/dists_xor/diffs.npy", 'b', 'o'])
    plist.append(["MEM, N=215", "../results/dists_mem/diffs.npy", 'k', 'v'])
    outfile = "../results/diffs_comparison.png"
    block_size = 40

    try:
        diff_percentage = float(sys.argv[1])
    except:
        diff_percentage = 20 

    fig = plt.figure()
    ax1 = fig.add_subplot(111)

    for row in plist:
        data = np.load(row[1])
#         diff_thresh = (1+(diff_percentage/100))*np.min(data[:,2])
#         print diff_thresh
        z = data[:,2]
        diff_thresh = np.percentile(z, diff_percentage)
        data = data[data[:,2] <= diff_thresh]
        x = data[:,0]
        y = data[:,1]

        ax1.scatter(x, y, s=block_size, alpha=0.5, label=row[0], c=row[2], marker=row[3])

    plt.xlabel("PTxJ")
    plt.ylabel("MCSxS")
    plt.legend(loc='upper left')
    plt.title("Lowest {:.0f}% of Distribution Difference".format(diff_percentage))
    plt.show()
