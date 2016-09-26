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


def get_comparison_data(names, exact):

    comp_data = []
    exact = (float)(exact)
    label = None
    
    for fname in names:
        fname_str = os.path.split(fname)[-1]
        print(fname_str)
        with open(fname, 'r') as fp:
            raw = json.load(fp)

        data = [string.split(x) for x in raw['data']]
        data = np.array(data)
        params = json.loads(raw['test_params'])

        avg = np.mean(data[:,0].astype(float))
        res = -100*(avg - exact)/exact
        Tau = (long)(params['steps'])
        label = "SA"
        if "P" in params:
            label = "QMC (PT = {:.2f})".format(params['P']*params['T'])
            #label = "QMC (PT = {:.2f})".format(params['P']*params['T']*(1e-5)) #use this for ising32
        comp_data.append((res, Tau))
    
    comp_data = np.asarray(comp_data)
    
    return comp_data, label


if __name__ == "__main__":

    fdir = sys.argv[1]
    exact = sys.argv[2]
    problem = sys.argv[3]
    
    qmc020 = []
    qmc100 = []
    qmc250 = []
    qmc500 = []
    qmc750 = []
    qmc990 = []
    qmc2000 = []
    qmc5000 = []
    qmc10000 = []
    sa_data = []
    
    for fname in os.listdir(fdir):
        if fnmatch.fnmatch(fname, 'qmc*_020.txt'):
            qmc020.append(os.path.join(fdir,fname))
        elif fnmatch.fnmatch(fname, 'qmc*_100.txt'):
            qmc100.append(os.path.join(fdir,fname))
        elif fnmatch.fnmatch(fname, 'qmc*_250.txt'):
            qmc250.append(os.path.join(fdir,fname))
        elif fnmatch.fnmatch(fname, 'qmc*_500.txt'):
            qmc500.append(os.path.join(fdir,fname))
        elif fnmatch.fnmatch(fname, 'qmc*_750.txt'):
            qmc750.append(os.path.join(fdir,fname))
        elif fnmatch.fnmatch(fname, 'qmc*_990.txt'):
            qmc990.append(os.path.join(fdir,fname))
        elif fnmatch.fnmatch(fname, 'qmc*_2000.txt'):
            qmc2000.append(os.path.join(fdir,fname))
        elif fnmatch.fnmatch(fname, 'qmc*_5000.txt'):
            qmc5000.append(os.path.join(fdir,fname))
        elif fnmatch.fnmatch(fname, 'qmc*_10000.txt'):
            qmc10000.append(os.path.join(fdir,fname))
        elif fnmatch.fnmatch(fname, 'sa*.txt'):
            sa_data.append(os.path.join(fdir,fname))

    for data in [qmc020, qmc100, qmc250, qmc500, qmc750, qmc990, qmc2000, qmc5000, qmc10000, sa_data]:
        if data == []:
            continue
        data, label = get_comparison_data(data, exact)
        data = data[data[:,1].argsort()]
        plt.plot(data[:,1], data[:,0], '-o', alpha=0.75, label=label)
	
    plt.axhline(y=0, linewidth=1,alpha=0.75,color='g',label='Exact')
    plt.yscale('symlog', linthreshy=.01)
    plt.xscale('symlog', linthreshy=.1)

    plt.ylabel('Percent Residual Energy Above Exact Solution')
    plt.xlabel('Number of Monte Carlo Steps')
    plt.legend(loc='best')
    plt.title('QMC vs SA Residual Energies for {}'.format(problem))
    plt.grid(True)
    plt.show()
    