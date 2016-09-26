#!/usr/bin/python

import numpy as np
import os
import string

import dist_sweeps

# Produce tets to sweep PTxJ and MCSxS across different annealing times

if __name__ == "__main__":

#     XOR
    files = []
    files.append(["../data/xor010/sol0.txt", "../results/xor010/"])
    files.append(["../data/xor040/sol0.txt", "../results/xor040/"])
    files.append(["../data/xor1e3/sol0.txt", "../results/xor1e3/"])
    files.append(["../data/xor2e3/sol0.txt", "../results/xor2e3/"])

    for infile, outdir in files:
        dist_sweeps.make_testfile(infile, outdir, "time_sweeps_xor.sh", 102, append=True)

#     MEMORY
    files = []
    files.append(["../data/mem010/sol0.txt", "../results/mem010/"])
    files.append(["../data/mem040/sol0.txt", "../results/mem040/"])
    files.append(["../data/mem1e3/sol0.txt", "../results/mem1e3/"])
    files.append(["../data/mem2e3/sol0.txt", "../results/mem2e3/"])

    for infile, outdir in files:
        dist_sweeps.make_testfile(infile, outdir, "time_sweeps_mem.sh", 215, append=True)
