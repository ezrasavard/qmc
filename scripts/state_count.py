#!/usr/bin/python

import fnmatch
import numpy as np
import os
import string
import sys

if __name__ == "__main__":

#     fname = sys.argv[1]
    files = []

    fdir = sys.argv[1]
    for fname in os.listdir(fdir):
        if (fnmatch.fnmatch(fname, '*dump*') and not fnmatch.fnmatch(fname, '*accepts')):
            files.append(fname)

    files.sort(key=str.lower)
    
    for fname in files:
        data = []
        with open(os.path.join(fdir,fname)) as fp:
            for i, line in enumerate(fp):
                if i == 0:
                    continue
                data.append(line)
                if i == 3e6: # I don't want to run out of RAM
                    break

        try:
            data = np.array([string.split(x) for x in data])
            data = np.unique(data[:,1])
        except:
            print("File: {:40s}\tNo usable data found".format(fname))
            continue

        data = np.sort(data).astype(float)
        diffs = []
        for i, E in enumerate(data):
            if i == 0:
                continue
            diffs.append(abs(data[i-1]-E))
        diffs = np.array(diffs)

#         print("Energy levels:")
#         print(data)
#         print("Energy gaps:")
#         print(diffs)
        
        try:
            mindiff = np.min(diffs)
        except:
            print("File: {:40s}\tUnique energies: {}".format(fname, data.size))
        else:
            print("File: {:40s}\tUnique energies: {}\tMin gap: {:.4f}".format(fname, data.size, mindiff))
#             print("Minimum energy gap found: {:.4f}".format(np.min(diffs)))
#             print("Count of minimum difference found: {0}".format((diffs[(diffs[:]==np.min(diffs))]).size))
#             print("Average energy gap found: {:.4f}\n".format(np.mean(diffs)))
