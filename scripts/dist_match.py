#!/usr/bin/python

import dwave
import fnmatch
import json
import math
import matplotlib.pyplot as plt
import numpy as np
import os
import string
import sys

def boltz_weighted_difference(Ex, Px, Qx, kT):

    D = 0
    Enet = 0
    for i, E in enumerate(Ex):
        x = math.exp(-E/kT)
        diff = abs(Px[i] - Qx[i])
        D += x*diff
        Enet += x

    return D/Enet

def calc_diffs(qmc_names, make_plots=True, kT=50, outfile="diffs.npy"):

    diff_data = []

    for fname in qmc_names:
        fname_str = os.path.split(fname)[-1]
        print("{}:".format(fname_str))
        with open(fname, 'r') as fp:
            raw = json.load(fp)

        data = [string.split(x) for x in raw['data']]
        data = np.array(data)
        params = json.loads(raw['test_params'])

        energies = data[:,0].astype(float)
        vectors = data[:,1]
        dwave_max = np.max(state_array)
        dwave_min = np.min(state_array)
        bottom = int(math.floor(min(np.min(energies), dwave_min)))
        top = int(math.ceil(max(np.max(energies), dwave_max)))
        bins = np.linspace(dwave_min, dwave_max, 20)

        # calculate dists and differences
        Px, Ex, _ = plt.hist(energies, bins, normed=True, orientation='horizontal',
                facecolor='green', alpha=1, label='QMC')

        Qx, _, _ = plt.hist(state_array, bins, normed=True, orientation='horizontal',
                facecolor='red', alpha=0.5, label='DWave')
        Ex = Ex[:-1]
        D = boltz_weighted_difference(Ex, Px, Qx, kT)

        diff_data.append((params['PTxJ'], params['MCSxS'], D))
#         if (D <= 0.08):
#             print("Difference: {:.5f}\t<---".format(D))
#         else:
#             print("Difference: {:.5f}".format(D))

        P_str = "P: {}".format(params['P'])
        PT_str = "PT: {:.4f}".format(params['P']*params['T'])
        Tau_str = "Tau: {}".format(params['steps'])
        PTxJ_str = "PTxJ: {}".format(params['PTxJ'])
        MCSxS_str = "MCSxS: {}".format(params['MCSxS'])
        N_str = "N: {}".format(params['N'])
        param_str = string.join([P_str, PT_str, Tau_str, PTxJ_str, MCSxS_str, N_str], "; ")

        if make_plots:
            plt.text(.1, bottom - .75*(bottom - top), "Difference: {:.5f}".format(D), fontsize=18)
            plt.ylabel('Energies')
            plt.xlabel('Number of Slices in State')
            plt.legend(loc='best')
            plt.title('Distribution for {}\n{}'.format(fname_str, param_str))
            plt.grid(True)
            plt.savefig(string.join([fname,"dist.png"],"_"), bbox_inches='tight', format='png')

        plt.close()

    diff_data = np.array(diff_data)
    fname = os.path.join(fdir, outfile)
    np.save(fname, diff_data)

if __name__ == "__main__":

    qmc_names = []
    outfile = "diffs.npy"
    if sys.argv[1] == "--qmc":
        fdir = sys.argv[2]
        for fname in os.listdir(fdir):
            if fnmatch.fnmatch(fname, '*.txt'):
                qmc_names.append(os.path.join(fdir,fname))

        qmc_names.sort(key=str.lower)
    elif sys.argv[1] == "--qmcfile":
        fdir, fname = os.path.split(sys.argv[2])
        qmc_names.append(sys.argv[2])
        outfile = string.split(fname,'.')[0] + "_diffs.npy"
        print outfile

    if sys.argv[3] == "--dwave":
        dwave_file = sys.argv[4]
        counts, e = dwave.load_jakes_dwave_data(dwave_file)
        state_array = []
        for i, count in enumerate(counts):
            state_array += [e[i] for x in range(0,count)]

    if "--sweep" in sys.argv:
        for kT in np.linspace(.5,50,10):
            outfile = "diffs_{}.npy".format(kT)
            calc_diffs(qmc_names, make_plots=False, kT=kT, outfile=outfile)
    else:
        calc_diffs(qmc_names, make_plots=True, kT=50, outfile=outfile)
