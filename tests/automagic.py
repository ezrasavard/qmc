#!/usr/bin/python

import numpy as np
import os
import string
import sys

if __name__ == "__main__":

    # directories are laid out to have "circuitname/runtime/files" in the path
    # traverse root directory, and list directories as dirs and files as files
    fname = "automagic.txt"
    trials = 100
    cmds = []
    for root, dirs, files in os.walk(sys.argv[1]):
        if 'sol0.txt' in files:
            path = os.path.relpath(root).split(os.sep)
            infile = os.path.join(root, "sol0.txt")
            outdir = os.path.join("../results", *path[-3:])
            outfile = os.path.join(outdir, fname)
            s = " ".join(["../solve", infile, outfile, "qmc", "--trials", str(trials),"--automagic"])
            cmds.append(s)

    testfile = "GENERATED_automagic.sh"
    with open(testfile,'w') as fp:
        fp.write("#!/bin/bash\n")
        for line in cmds:
            fp.write(line)
            fp.write('\n')
