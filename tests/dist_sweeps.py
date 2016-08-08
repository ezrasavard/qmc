#!/usr/bin/python

import numpy as np
import os
import string

# Produce tests to sweep PTxJ and MCSxS

PTxJ = np.linspace(1,100,20).astype(int)

def qmc_string(infile, outdir, PTxJ, MCSxS, trials=100, P=60, sched="../data/schedule.txt"):

    fname = string.join(["{:03d}".format(PTxJ), "_", "{:04d}".format(MCSxS), ".txt"],"")
    outfile = os.path.join(outdir, fname)
    s = " ".join(["../solve", infile, outfile, "qmc", "--trials", str(trials),
            "--P", str(P), "--PTxJ", str(PTxJ), "--MCSxS", str(MCSxS), "--schedule",
            sched])

    return s

def make_testfile(infile, outdir, testfile, N, append=False):

    cmds = []
    for coupling in PTxJ:
        for MCS in MCSxS(N):
            cmds.append(qmc_string(infile, outdir, coupling, MCS))

    mode = 'w'
    if append:
        mode = 'a'
    with open(testfile, mode) as fp:
        fp.write("#!/bin/bash\n")
        for line in cmds:
            fp.write(line)
            fp.write('\n')

def MCSxS(N):

    return np.linspace(10,10*N,len(PTxJ)).astype(int)


if __name__ == "__main__":


#     XOR 102 spins
    make_testfile("../data/xor100/sol0.txt", "../results/dists_xor/", "dist_sweeps_xor.sh", 102)

#     MAJ 14 spins
    make_testfile("../data/maj531/sol0.txt", "../results/dists_maj/", "dist_sweeps_maj.sh", 14)

#     MEMORY 215 spins
    make_testfile("../data/mem100/sol0.txt", "../results/dists_mem/", "dist_sweeps_mem.sh", 215)

#     S3INV 52 spins
    make_testfile("../data/s3inv20/sol0.txt", "../results/dists_inv/", "dist_sweeps_inv.sh", 52)
