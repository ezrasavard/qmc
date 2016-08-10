#!/usr/bin/python

import numpy as np
import os
import string
import sys

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

    if not os.path.exists(os.path.dirname(outdir)):
        os.makedirs(os.path.dirname(outdir))

def MCSxS(N):

    return np.linspace(10,10*N,len(PTxJ)).astype(int)

def get_N(infile):

    data = np.loadtxt(infile, skiprows=1)
    spins = np.unique(data[:,(0,1)])
    return len(spins)


if __name__ == "__main__":

    # directories are laid out to have "circuitname/runtime/files" in the path
    # traverse root directory, and list directories as dirs and files as files
    for root, dirs, files in os.walk(sys.argv[1]):
        if 'sol0.txt' in files:
            path = os.path.relpath(root).split(os.sep)
            infile = os.path.join(root, "sol0.txt")
            outdir = os.path.join("../results", *path[-3:])
            outfile = string.join(["GENERATED", path[-2], path[-1], "sweep.sh"],"_")
            N = get_N(infile)
            print("{}\n{}\n{}\n{}\n".format(infile, outdir, outfile, N))
            make_testfile(infile, outdir, outfile, N)
