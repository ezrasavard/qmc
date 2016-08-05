#!/usr/bin/python

import numpy as np
import os
import string

# Try Tau = 100 MCS/spin, PT = 20*<|J|>

# Sweep PTxJ and MCSxS
# 50 <= MCSxS <= 2*N
# 1 <= PTxJ <= 100

def qmc_string(infile, outdir, PTxJ, MCSxS, trials=100, P=60):

    fname = string.join(["{:03d}".format(PTxJ), "_", "{:04d}".format(MCSxS), ".txt"],"")
    outfile = os.path.join(outdir, fname)
    s = " ".join(["../solve", infile, outfile, "qmc", "--trials", str(trials),
            "--P", str(P), "--PTxJ", str(PTxJ), "--MCSxS", str(MCSxS)])

    return s

if __name__ == "__main__":

    PTxJ = np.linspace(1,100,20).astype(int)
    MCSxS = lambda N: np.linspace(10,10*N,len(PTxJ)).astype(int)

#     SPLIT2
    cmds = []
    N = 27
    files = []
    files.append(["../data/split2/sol0.txt", "../results/split2/"])

    for infile, outdir in files:
        for coupling in PTxJ:
            for MCS in MCSxS(N):
                cmds.append(qmc_string(infile, outdir, coupling, MCS))

#     SPLIT3
    N = 42
    files = []
    files.append(["../data/split3/sol0.txt", "../results/split3/"])

    for infile, outdir in files:
        for coupling in PTxJ:
            for MCS in MCSxS(N):
                cmds.append(qmc_string(infile, outdir, coupling, MCS))

    with open('splits.sh','w') as fp:
        fp.write("#!/bin/bash\n")
        for line in cmds:
            fp.write(line)
            fp.write('\n')

