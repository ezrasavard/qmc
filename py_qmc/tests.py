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

    try:
        data_file = sys.argv[1]
    except:
#         data_file = 'data/coefs0.txt'
#         scale = 1
        data_file = 'data/ising32.txt'
        scale = 1e-5
        print('No data file specified, '
                'using default test data file: ' + data_file)

    filename = data_file.split('/')[-1]
    tmp = filename.split('.')
    filename = tmp[-2]
    ext = tmp[-1]

    problems = []
    if ext == 'qca':
        h_list, J_n, poles = qca.exact_solve(data_file, ret=True, solve=False)
        for i, h in enumerate(h_list):
            p = problem.ising(hJ=(h,J_n))
            exacts, soln_vects, modes = rp.rp_solve(h, J_n, 0.1)
            p.exact = float(exacts[0])
            p.poles = copy.copy(h)
            p.initial_energy = p.get_E(p.spins)
            print p.initial_energy
            problems.append(p)
    else:
        p = problem.ising(data_file, scale=scale)
#         p.exact = -98.266
        p.exact = -136200386.56*scale*1024
        p.initial_energy = p.get_E()
        print "Problem initial energy: {:.2f}".format(p.initial_energy)
        print "Problem initial spins:"
        print p.spins
        problems.append(p)


    steps = 1e5
    test = {"G0":10,"Gf":0.1,"T0":3,"T":0.015,"Epf":1,"steps":steps,"P":40}

    for p in problems:
#         try:
#             lib_tests.QMC_vs_SA_real_time(p, test, p.exact, filename)
#         except Exception as e:
#             print e
#             print "real time failed"
#         try:
        lib_tests.QMC_vs_SA_sweep_steps(p, test, p.exact, filename)
#         except Exception as e:
#             print e
#             print "step sweep failed"
#         try:
#             lib_tests.QMC_vs_SA_sweep_Epf(p, test, p.exact, filename)
#         except Exception as e:
#             print e
#             print "Epf sweep failed"
#         try:
#             lib_tests.QMC_real_time_sweep_params(p, filename)
#         except Exception as e:
#             print e
#             print "real time param sweep failed"
#         try:
#             lib_tests.QMC_final_distributions(p, test, filename)
#         except Exception as e:
#             print e
#             print "final distributions failed"
