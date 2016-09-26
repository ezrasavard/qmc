#!/usr/bin/python

# a file for calling my tests

import copy
import numpy as np
import string
import sys

import lib_tests
import problem
import qca_embed.new_src.qca_solver as qca
import qca_embed.new_src.solvers.rp_solve as rp
import qmc


if __name__=="__main__":

    data_file = 'data/ising32.txt'
    scale = 1e-5

    filename = 'ising32'

    problems = []
    p = problem.ising(data_file, scale=scale)
    p.exact = -133008.19*scale*1024
    p.initial_energy = p.get_E()
    print "Problem initial energy: {:.2f}".format(p.initial_energy)
    print "Problem initial spins:"
    print p.spins
    problems.append(p)

    steps = 1e5
    test = {"G0":10,"Gf":0.1,"T0":3,"T":0.010,"Ep0":0.1,"Epf":1,"steps":steps,"P":30}

    for p in problems:
#         lib_tests.QMC_vs_SA_real_time(p, test, p.exact, filename)
        lib_tests.QMC_vs_SA_sweep_steps(p, test, p.exact, filename)
