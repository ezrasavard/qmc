#!/usr/bin/python

import numpy as np
import string

import qca_embed.new_src.solvers.rp_solve as rp

class ising():

    def __init__(self, data_file='data/coefs0.txt', hJ=None, randomize=True, scale=1, fname=None):
        # data_file: a list of (i j coupling) tuples or a QCADesigner file
        # hJ: tuple of h and J matrices, instead of data_file
        #     expected to be a vector and symmetric matrix, respectively
        # randomize: random spin configuration, otherwise +1 for all spins

        filename = data_file.split('/')[-1]
        tmp = filename.split('.')
        filename = tmp[-2]
        ext = tmp[-1]

        if hJ:
            # import from QCADesigner
            h = hJ[0]
            J = np.tril(hJ[1]) # using lower triangular
            count = len(J[0])
        else:
            data = np.loadtxt(data_file, skiprows=1)
            max_spin_ind = int(np.amax(data[:,(0,1)]))

            # map spins to a reduced set
            original_spin_map = np.unique(data[:,(0,1)]).astype(int)
            spin_map = np.zeros((max_spin_ind+1),dtype=int)
            for i, spin in enumerate(original_spin_map):
                spin_map[spin] = i

            count = len(original_spin_map) # number of spins to consider

            # build a reduced matrix of spin couplings
            # this is lower triangular with self-couplings on the diagonal
            # indexed from 0 and using spins mapped to sequential integers
            J = np.zeros((count, count),dtype=float)
            for row in data:
                j = spin_map[row[0]]
                i = spin_map[row[1]]
                J[i,j] = row[2]
            h = np.diag(J)
            np.fill_diagonal(J,0)

        if randomize:
            # initialized to a random strong coupling configuration if desired
            spins = (np.random.rand(count) > .5).astype(int)
            spins[spins == 0] = -1
        else:
            spins = np.ones(count, dtype=int)


        self.spins = spins
        self.N = count
        self.h = h*scale
        self.J = J*scale
        self.poles = None
        self.initial_energy = None
        self.exact = None
        self.filename = fname


    def get_E(self, spins=None):
        # returns total energy
        # can only be used on problems with fewer than 100 spins reliably

        if spins is None:
            spins = self.spins

        # self couplings
        E = np.dot(spins, self.h)

        # slice local couplings
        x = np.dot(spins, self.J)
        E += np.dot(spins, x)

        return E
