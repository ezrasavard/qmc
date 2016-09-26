#!/usr/bin/python

# a file for calling my tests

import copy
import numpy as np
import string
import sys
import time

import dwave_distributions as dwave
import lib_tests
import matplotlib.pyplot as plt
import problem
import qca_embed.new_src.qca_solver as qca
import qca_embed.new_src.solvers.rp_solve as rp
import qmc


if __name__=="__main__":

    data_file = 'data/ising32.txt'
    scale = 1e-5

    filename = 'ising32'

    problems = []
    p = problem.ising(data_file, scale=scale, fname=filename)
    p.exact = -133008.19*scale*1024
    p.initial_energy = p.get_E()
    print "Problem initial energy: {:.2f}".format(p.initial_energy)
    print "Problem initial spins:"
    problems.append(p)

    steps_list = [1e2, 1e3, 1e4, 1e5]
#     steps_list = [1e2, 1e3]
    N = 10
    tests = []

    # PT = 0.3
    tests.append({"G0":10,"Gf":0.1,"T":0.015,"Ep0":0.1,"Epf":1,"P":20})
    tests.append({"G0":10,"Gf":0.1,"T":0.0075,"Ep0":0.1,"Epf":1,"P":40})
    tests.append({"G0":10,"Gf":0.1,"T":0.005,"Ep0":0.1,"Epf":1,"P":60})

    # PT = 0.6
    tests.append({"G0":10,"Gf":0.1,"T":0.03,"Ep0":0.1,"Epf":1,"P":20})
    tests.append({"G0":10,"Gf":0.1,"T":0.015,"Ep0":0.1,"Epf":1,"P":40})
    tests.append({"G0":10,"Gf":0.1,"T":0.010,"Ep0":0.1,"Epf":1,"P":60})

    plt.figure()
    plt.hold(True)
    for p in problems:
#         plot residual energy vs computation time
#         for each set of params

        sa_energy = []
        sa_time = []
        for steps in steps_list:
            energies = []
            times = []
            for k in range(N):
                s = qmc.SimulatedAnnealing(p,3,1e-4,steps=steps)

                # time QMC
                t1 = time.time()
                s.anneal()
                t2 = time.time()
                t_sa = t2 - t1
                print('SA time: {:.4f}'.format(t_sa))
                energies.append(s.final_energy)
                times.append(t_sa)
            sa_energy.append(np.mean(energies) - p.exact)
            sa_time.append(1e3*np.mean(times))
        plt.plot(sa_time, sa_energy, 'o-', markersize=10, label="SA", alpha=0.5)

        for t in tests:
            final_dists = np.zeros((N,t['P']))
            qmc_energy = []
            qmc_time = []
            for steps in steps_list:
                energies = []
                times = []
                for k in range(N):
                    s = qmc.PIMC(p,P=t['P'],G0=t['G0'],Gf=t['Gf'],T=t['T'],Ep0=t['Ep0'],Epf=t['Epf'],steps=steps)

                    # time QMC
                    t1 = time.time()
                    s.solve()
                    t2 = time.time()
                    t_qmc = t2 - t1
                    print('QMC time: {:.4f}'.format(t_qmc))
                    energies.append(s.final_energy)
                    times.append(t_qmc)
                    final_dists[k,:] = s.data['final_slice_energies']
                qmc_energy.append(np.mean(energies) - p.exact)
                qmc_time.append(1e3*np.mean(times))

            label = "P={0}; T={1}".format(t['P'],t['T'])
            plt.plot(qmc_time, qmc_energy, 'o-', markersize=10, label=label, alpha=0.5)

    filename = string.join(['images/test_ising32_', time.strftime("%Y-%m-%d_%H-%M-%S"), '.svg'], '')

    plt.ylabel('Residual Energy')
    plt.axhline(y=0, linewidth=1,alpha=0.75,color='g')
    plt.yscale('symlog', linthreshy=0.1)
    plt.xscale('symlog', linthreshy=0.1)
    plt.ylim(-1e-2,1e4)
    plt.xlabel('Computation Time (ms)')
    plt.legend(loc='best')
    plt.title('Ising32 at Various PT Values')
    plt.grid(True)
    plt.savefig(filename, bbox_inches='tight', format='svg', dpi=1200)
    plt.close()
