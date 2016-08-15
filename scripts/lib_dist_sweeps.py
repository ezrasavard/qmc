#!/usr/bin/python

import lib_dwave as dwave
import fnmatch
import json
import math
import matplotlib.pyplot as plt
import numpy as np
import os
import string
import sys

def make_heatmap(data, title, outfile):

    if type(data) != np.array:
        # data might be an npy file instead of an array
        data = np.load(data)

    x = data[:,0]
    y = data[:,1]
    z = data[:,2]

    block_size = (np.max(x) - np.min(x))**2
    plt.scatter(x,y,c=z,s=block_size,edgecolors='face',marker='s')
    plt.xlim(np.min(x),np.max(x))
    plt.ylim(np.min(y),np.max(y))
    plt.xlabel("PTxJ")
    plt.ylabel("MCSxS")
    cb = plt.colorbar()
    cb.set_label('Differences')
    plt.title(title)
    plt.savefig(outfile, bbox_inches='tight', format='png')


def best_diffs(data, diff_percentage=5, outfile='../results/diffs_comparison.png', block_size=40, ret=False, plot=True):

    if type(data) != np.array:
        # data might be an npy file instead of an array
        data = np.load(data)
    z = data[:,2]
    diff_thresh = np.percentile(z, diff_percentage)
    data = data[data[:,2] <= diff_thresh]
    x = data[:,0]
    y = data[:,1]

    if plot:
        fig = plt.figure()
    #     ax1 = fig.add_subplot(111)
    #     ax1.scatter(x, y, s=block_size, alpha=0.5, label=row[0], c=row[2], marker=row[3])
        plt.scatter(x, y, s=block_size, alpha=0.5, label=row[0], c=row[2], marker=row[3])

        plt.xlabel("PTxJ")
        plt.ylabel("MCSxS")
        plt.legend(loc='upper left')
        plt.title("Lowest {:.0f}% of Distribution Difference".format(diff_percentage))
        plt.grid(True)
        plt.savefig(string.join([fname,"dist.png"],"_"), bbox_inches='tight', format='png')

    if ret:
        return data


def boltz_weighted_difference(Ex, Px, Qx, kT):

    D = 0
    Enet = 0
    for i, E in enumerate(Ex):
        x = math.exp(-E/kT)
        diff = abs(Px[i] - Qx[i])
        D += x*diff
        Enet += x

    return D/Enet

def calc_diffs(qmc_names, make_plots=True, kT=50, outfile="diffs.npy", ret=False):

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

    if ret:
        return diff_data

