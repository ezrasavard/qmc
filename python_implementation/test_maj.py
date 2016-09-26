#!/usr/bin/python

import copy
import numpy as np
import string
import sys

import dwave_distributions as dwave
import lib_tests
import problem
import qca_embed.new_src.qca_solver as qca
import qca_embed.new_src.solvers.rp_solve as rp
import qmc


if __name__=="__main__":

    data_file = 'primitives/maj/maj-531.qca'
    dwave_file = 'data/maj-531_8.json'
    h, J, counts, e = dwave.load_dwave_data(dwave_file)
    filename = 'maj531'

    problems = []
    exacts, soln_vects, modes = rp.rp_solve(h, J, 0)
    print h
    input_cells = [0, 3, 11]
    inputs = np.rint(h[input_cells]).astype(int)
    print inputs
    p = problem.ising(hJ=(h,J), fname=filename)
    p.exact = float(exacts[0])
    p.poles = inputs
    p.initial_energy = p.get_E()

    steps = 1e2
    N = 40
    tests = []

    tests.append({"G0":10,"Gf":0.1,"T":0.015,"Ep0":0.1,"Epf":1,"steps":steps,"P":20})
    tests.append({"G0":10,"Gf":0.1,"T":0.0075,"Ep0":0.1,"Epf":1,"steps":steps,"P":40})
    tests.append({"G0":10,"Gf":0.1,"T":0.005,"Ep0":0.1,"Epf":1,"steps":steps,"P":60})
    tests.append({"G0":10,"Gf":0.1,"T":0.03,"Ep0":0.1,"Epf":1,"steps":steps,"P":20})
    tests.append({"G0":10,"Gf":0.1,"T":0.015,"Ep0":0.1,"Epf":1,"steps":steps,"P":40})
    tests.append({"G0":10,"Gf":0.1,"T":0.010,"Ep0":0.1,"Epf":1,"steps":steps,"P":60})
#     tests.append({"G0":10,"Gf":0.1,"T":0.010,"Ep0":0.1,"Epf":1,"steps":10*steps,"P":30})
#     tests.append({"G0":10,"Gf":0.1,"T":0.010,"Ep0":0.1,"Epf":1,"steps":100*steps,"P":30})

    for t in tests:
        print "test params:"
        print t
        energies = np.zeros((N,t['P']))
        for k in range(N):
            print "iteration: {0}".format(k)
            s = qmc.PIMC(p,P=t['P'],G0=t['G0'],Gf=t['Gf'],T=t['T'],Ep0=t['Ep0'],Epf=t['Epf'],steps=t['steps'])
            s.solve()
            energies[k,:] = s.data['final_slice_energies']

        params = lib_tests.make_param_string(t,s)
        params += '\nInputs ' + str(p.poles)
        data = energies.flatten()
        tcounts = counts*N*float(t['P'])/np.sum(counts)
        lib_tests.plot_final_slice_histogram(data, s.P, params, filename, ylims=(-13,0), actuals=(tcounts,e))
