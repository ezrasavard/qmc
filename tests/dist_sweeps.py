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

#     XOR 102 spins
    cmds = []
    N = 102
    infile = "../data/xor100/sol0.txt"
    outdir = "../results/dists_xor/"

    for coupling in PTxJ:
        for MCS in MCSxS(N):
            cmds.append(qmc_string(infile, outdir, coupling, MCS))

    with open('dist_sweeps_xor.sh','w') as fp:
        fp.write("#!/bin/bash\n")
        for line in cmds:
            fp.write(line)
            fp.write('\n')

#     MAJ 14 spins
    cmds = []
    N = 14
    infile = "../data/maj531/sol0.txt"
    outdir = "../results/dists_maj/"

    for coupling in PTxJ:
        for MCS in MCSxS(N):
            cmds.append(qmc_string(infile, outdir, coupling, MCS))

    with open('dist_sweeps_maj.sh','w') as fp:
        fp.write("#!/bin/bash\n")
        for line in cmds:
            fp.write(line)
            fp.write('\n')

#     MEMORY 215 spins
    cmds = []
    N = 215
    infile = "../data/mem100/sol0.txt"
    outdir = "../results/dists_mem/"

    for coupling in PTxJ:
        for MCS in MCSxS(N):
            cmds.append(qmc_string(infile, outdir, coupling, MCS))

    with open('dist_sweeps_mem.sh','w') as fp:
        fp.write("#!/bin/bash\n")
        for line in cmds:
            fp.write(line)
            fp.write('\n')

#     S3INV 52 spins, <|J|> = 0.019
    cmds = []
    N = 52
    infile = "../data/s3inv20/sol0.txt"
    outdir = "../results/dists_inv/"

    for coupling in PTxJ:
        for MCS in MCSxS(N):
            cmds.append(qmc_string(infile, outdir, coupling, MCS))

    with open('dist_sweeps_inv.sh','w') as fp:
        fp.write("#!/bin/bash\n")
        for line in cmds:
            fp.write(line)
            fp.write('\n')

