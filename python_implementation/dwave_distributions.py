#!/usr/bin/python

import demjson
import json
import matplotlib.pyplot as plt
import numpy as np
import sys

def load_raw_dwave_data(fname):

    with open(fname, 'r') as fp:
        data = json.load(fp)

    e = np.array(data['all_energies'])
    occ = np.array(data['all_hwocc'])

    uniques, inds = np.unique(e,return_index=True)
    countsets = []
    inds = list(inds)
    inds.append(-1)
    left = inds.pop(0)
    for i in inds:
        countsets.append(np.sum(occ[left:i]))
        left = i
    countsets = np.array(countsets)

    return countsets, uniques


def load_dwave_data(fname):
    
    with open(fname, 'r') as fp:
        data = json.load(fp)
    
    h_ = data['h']
    J_ = data['J']
    qbits = data['qbits']
    N = len(qbits)
    e = np.array(data['energies'])
    occ = np.array(data['occ'])
    
    h = np.zeros([N,], dtype=float)
    J = np.zeros([N, N], dtype=float)
    
    qbit_map = {qb: i for i, qb in enumerate(qbits)}
    
    for i, v in h_.iteritems():
        h[qbit_map[int(i)]] = v
    
    for i in J_:
        for j, v in J_[i].iteritems():
            J[qbit_map[int(i)], qbit_map[int(j)]] = v
            J[qbit_map[int(j)], qbit_map[int(i)]] = v
    
    uniques, inds = np.unique(e,return_index=True)
    countsets = []
    inds = list(inds)
    inds.append(-1)
    left = inds.pop(0)
    for i in inds:
        countsets.append(np.sum(occ[left:i]))
        left = i
    countsets = np.array(countsets)

    return h, J, countsets, uniques

def make_hJ_json(fname, hJ_file, outfile):
    # not yet functional
    # need to implement the qubit mappings etc.
    # not worth the trouble right now

    data = {}
    with open(fname, 'r') as fp:
        res_data = json.load(fp)

    hJ_data = np.loadtxt(hJ_file, skiprows=1)
    max_spin_ind = int(np.amax(hJ_data[:,(0,1)]))

    original_spin_map = np.unique(hJ_data[:,(0,1)]).astype(int)
    spin_map = np.zeros((max_spin_ind+1),dtype=int)
    for i, spin in enumerate(original_spin_map):
        spin_map[spin] = i
    count = len(original_spin_map) # number of spins to consider
    J = np.zeros((count, count),dtype=float)
    for row in data:
        j = spin_map[row[0]]
        i = spin_map[row[1]]
        J[i,j] = row[2]
    h = np.diag(J)
    np.fill_diagonal(J,0)
    J += np.transpose(J)
    print J

    data['qbits'] = res_data['usedqubits']
    data['energies'] = res_data['all_energies']
    data['occ'] = res_data['all_hwocc']
    data['h'] = list(h)
    data['J'] = list(J)

    with open(outfile, 'w') as fp:
        fp.write(json.dumps(data))


if __name__ == "__main__":

    h, J, countsets, uniques = load_dwave_data(sys.argv[1])
    plt.scatter(countsets, uniques)
    plt.show()
    
#     make_hJ_json('data/xor.json', 'data/coefs0.txt', 'data/test_json.json')
