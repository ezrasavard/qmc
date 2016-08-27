#!/usr/bin/python

import lib_dwave as dwave
import fnmatch
import json
import math
import matplotlib.pyplot as plt
import numpy as np
import os
from scipy.optimize import curve_fit
import string
import sys

class Transformer(object):

    def __init__(self, data, N):

        self.data = data
        x = data[:,0]
        y = data[:,1]
        print("x: \n{}".format(x))
        print("y: \n{}".format(y))
        self.xmed = np.median(x)
        self.N = N
        self.mcsxs_args, _ = curve_fit(self.MCSxSfunc, x, y, maxfev=1000000)
        self.curve_data = [[ptxj, self.MCSxSfunc(ptxj, *self.mcsxs_args)] for ptxj in x]

    def MCSxSfunc(self, x, k1, k2, k3, k4):

        fN = np.log(self.N)*self.N

        return k1*(x**k2)*(fN**k3 + k4)


def fit_PTxJ(xmed, N):
    # xmed and N are arrays

    return curve_fit(PTxJfunc, N, xmed, maxfev=100000)[0]

def PTxJmap(args):

    return "PTxJ: N -> {:3f} * (NlogN)^{:3f}".format(*args)

def MCSxSmap(args):
    return "MCSxS: PTxJ, N -> {:3f} * (PTxJ^{:3f}) * ((NlogN)^{:3f} + {:3f})".format(*args)


def PTxJfunc(N, a, b):

    return a*((np.log(N)*N)**b)


def make_heatmap(data, title, outfile, data_is_file=False):

    if data_is_file:
        # data might be an npy file instead of an array
        data = np.load(data)

    x = data[:,0]
    y = data[:,1]
    z = data[:,2]

    block_size = (np.max(x) - np.min(x))**2
    plt.figure()
    plt.scatter(x,y,c=z,s=block_size,edgecolors='face',marker='s')
    plt.xlim(np.min(x),np.max(x))
    plt.ylim(np.min(y),np.max(y))
    plt.xlabel("PTxJ")
    plt.ylabel("MCSxS")
    cb = plt.colorbar()
    cb.set_label('Differences')
    plt.title(title)
    plt.savefig(outfile, bbox_inches='tight', format='png')
    plt.close()


def best_diffs(data, diff_percentage=5, outfile='../results/diffs_comparison.png', block_size=40, ret=False, plot=True, data_is_file=False):

    if data_is_file:
        # data might be an npy file instead of an array
        data = np.load(data)
    z = data[:,2]
    diff_thresh = np.percentile(z, diff_percentage)
    data = data[data[:,2] <= diff_thresh]
    x = data[:,0]
    y = data[:,1]

    if plot:
        fig = plt.figure()
        plt.scatter(x, y, s=block_size, alpha=0.5, label=row[0], c=row[2], marker=row[3])

        plt.xlabel("PTxJ")
        plt.ylabel("MCSxS")
        plt.legend(loc='upper left')
        plt.title("Lowest {:.0f}% of Distribution Difference".format(diff_percentage))
        plt.grid(True)
        plt.savefig(string.join([fname,"dist.png"],"_"), bbox_inches='tight', format='png')

    if ret:
        if data == []:
            raise Exception("empty data for file: {}".format(outfile))
        return data


def boltz_weighted_difference(Ex, Px, Qx, kT):

    D = 0
    Enet = 0
    overlap = False
    for i, P in enumerate(Px):
        if P != 0 and Qx[i] != 0:
            overlap = True
            break

    if overlap == False:
        # no overlap at all == diff of 1
        return 1.0

    for i, E in enumerate(Ex):
        if Px[i] == 0 and Qx[i] == 0:
            # no contribution from both empty
            continue
        x = math.exp(-E/kT)
        diff = abs(Px[i] - Qx[i])
        D += 3*x*diff
        Enet += x

    return D/Enet

def calc_diffs(qmc_names, dwave_file, make_plots=True, kT=50, outfile="diffs.npy", ret=False):

    diff_data = []

    counts, e = dwave.load_jakes_dwave_data(dwave_file)
    state_array = []
    for i, count in enumerate(counts):
        state_array += [e[i] for x in range(0,count)]

    for fname in qmc_names:
        fname_str = os.path.split(fname)[-1]
#         print("calc diffs for: {}".format(fname_str))
        with open(fname, 'r') as fp:
            raw = json.load(fp)

        data = [string.split(x) for x in raw['data']]
        data = np.array(data)
        params = json.loads(raw['test_params'])

        energies = data[:,0].astype(float)
        vectors = data[:,1]
        dwave_max = np.max(state_array)
        dwave_min = np.min(state_array)
        qmc_max = np.max(energies)
        qmc_min = np.min(energies)
        bottom = int(math.floor(min(qmc_min, dwave_min)))
        top = int(math.ceil(max(qmc_max, dwave_max)))
        bins = np.linspace(bottom, top, (top-bottom)) # bin at every integer energy

        # calculate dists and differences
        plt.figure()
        Px, Ex, _ = plt.hist(energies, bins, normed=True, orientation='horizontal',
                facecolor='green', alpha=1, label='QMC')

        Qx, _, _ = plt.hist(state_array, bins, normed=True, orientation='horizontal',
                facecolor='red', alpha=0.5, label='DWave')
        Ex = Ex[:-1]
        kT = max(abs(Ex))/2
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
            plt.ylabel('Energies')
            plt.xlabel('Percentage of Results in State')
            plt.ylim((-2*kT, 0))
            plt.xlim((0,1))
            plt.legend(loc='best')
            plt.title('Distribution for {}\n{}\nDifference: {:4f}'.format(fname_str, param_str, D))
            plt.grid(True)
            plt.savefig(string.join([fname,"dist.png"],"_"), bbox_inches='tight', format='png')
        plt.close()

    diff_data = np.array(diff_data)
    np.save(outfile, diff_data)

    if ret:
        return diff_data

def get_N(infile):

    print("Getting N from: {}".format(infile))
    data = np.loadtxt(infile, skiprows=1)
    spins = np.unique(data[:,(0,1)])
    return len(spins)
