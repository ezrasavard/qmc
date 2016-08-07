#!/usr/bin/python

import matplotlib.pyplot as plt
import numpy as np
import sys

from scipy.optimize import curve_fit

def proto_cubic(t, a3, a2, a1, a0):

    if type(t) == list:
        return [proto_cubic(x, a3, a2, a1, a0) for x in t]
    else:
        return a3*t**3 + a2*t**2 + a1*t + a0

if __name__ == "__main__":

    infile = sys.argv[1]
    outfile = sys.argv[2]
    plot = False

    try:
        plot = (sys.argv[3] == "--plot")
    except:
        pass

    lines = [x for x in range(1001)] # 1001 data points
    data = np.loadtxt(infile).astype(float)
    g = data[:,1]
    ep = data[:,2]
    try:
        assert(g.size == 1001)
    except:
        print("error: expected data to have 1001 rows")
        print(g)
        print(g.size)
    gcoeffs, _ = curve_fit(proto_cubic, lines, g)
    epcoeffs, _ = curve_fit(proto_cubic, lines, ep)

    with open(outfile, "w+") as f:
        f.write("{:f} {:f} {:f} {:f} {:f} {:f}\n".format(g[0], g[-1], *gcoeffs))
        f.write("{:f} {:f} {:f} {:f} {:f} {:f}\n".format(ep[0], ep[-1], *epcoeffs))

    if plot:
        plt.subplot(2, 1, 1)
        plt.plot(lines, g, color='b',linewidth=2)
        plt.title("Annealing Schedule")
        plt.ylabel("Gamma value, normalized")
        plt.subplot(2, 1, 2)
        plt.plot(lines, ep, color='g', linewidth=2)
        plt.ylabel("Epsilon value, normalized")
        plt.xlabel("time, normalized to 1000 time-steps")
        plt.show()
