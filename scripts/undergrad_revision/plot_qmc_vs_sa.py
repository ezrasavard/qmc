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


def get_comparison_data(names):

    comp_data = []
    
    for fname in names:
        fname_str = os.path.split(fname)[-1]
        print(fname_str)
        with open(fname, 'r') as fp:
            raw = json.load(fp)

        data = [string.split(x) for x in raw['data']]
        data = np.array(data)
        params = json.loads(raw['test_params'])

        avg = np.mean(data[:,0].astype(float))
        Tau = (long)(params['steps'])
        comp_data.append((avg, Tau))
    
    return comp_data
    
    
def make_plot(qmc_data, sa_data, exact, problem):

    exact = (float)(exact)
    qmc_data = np.asarray(qmc_data)
    sa_data = np.asarray(sa_data)
    qmc_data[:,0] = -100*(qmc_data[:,0] - exact)/exact
    sa_data[:,0] = -100*(sa_data[:,0] - exact)/exact

    qmc_data = qmc_data[qmc_data[:,1].argsort()]
    sa_data = sa_data[sa_data[:,1].argsort()]

    plt.plot(qmc_data[:,1], qmc_data[:,0], '-o', alpha=0.75, label='QMC')
    plt.plot(sa_data[:,1], sa_data[:,0], '-x', alpha=0.75, label='SA')

    plt.axhline(y=0, linewidth=1,alpha=0.75,color='g',label='Exact')
    plt.yscale('symlog', linthreshy=1)
    plt.xscale('symlog', linthreshy=1)

    plt.ylabel('Percent Residual Energy Above Exact Solution')
    plt.xlabel('Number of Monte Carlo Steps')
    plt.legend(loc='best')
    plt.title('QMC vs SA Residual Energies for {}'.format(problem))
    plt.grid(True)
    plt.show()
    
if __name__ == "__main__":

    qmc_names = []
    sa_names = []
    fdir = sys.argv[1]
    exact = sys.argv[2]
    for fname in os.listdir(fdir):
        if fnmatch.fnmatch(fname, 'qmc*.txt'):
            qmc_names.append(os.path.join(fdir,fname))
        elif fnmatch.fnmatch(fname, 'sa*.txt'):
            sa_names.append(os.path.join(fdir,fname))

    qmc_data = get_comparison_data(qmc_names)
    sa_data = get_comparison_data(sa_names)
	
    make_plot(qmc_data, sa_data, exact, sys.argv[3])
