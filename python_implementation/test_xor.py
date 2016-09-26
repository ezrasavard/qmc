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

    data_file = 'data/coefs0.txt'
    exact = -98.266
    dwave_file = 'data/xor.json'
    counts, e = dwave.load_raw_dwave_data(dwave_file)
    filename = 'xor-gate'

    problems = []
    p = problem.ising(data_file, fname=filename)
    p.exact = exact
    p.initial_energy = p.get_E()
    print p.filename
    print p.initial_energy
    print p.exact
    problems.append(p)

    steps_list = [1e2, 1e3, 1e4, 1e5]
    N = 5
    tests = []

    # PT = 0.3
    # best param selection so far
    tests.append({"G0":10,"Gf":0.1,"T":0.005,"Ep0":0.1,"Epf":1,"P":60})
    # slightly lower temp performed better still
    tests.append({"G0":10,"Gf":0.1,"T":0.003,"Ep0":0.1,"Epf":1,"P":60})

    # sweep lower temps, lower PTs
    tests.append({"G0":10,"Gf":0.1,"T":0.002,"Ep0":0.1,"Epf":1,"P":60})
    tests.append({"G0":10,"Gf":0.1,"T":0.001,"Ep0":0.1,"Epf":1,"P":60})

    # limiting case
    tests.append({"G0":10,"Gf":0.1,"T":0.0005,"Ep0":0.1,"Epf":1,"P":600})

    # sweeping epsilon outperformed not sweeping it
    # higher initial gamma was similar to epsilon sweep, a bit worse
#     tests.append({"G0":20,"Gf":0.1,"T":0.005,"Ep0":1,"Epf":1,"P":60})
    # consider testing a variety around PT = 0.3
    # increasing P makes PT higher, is worse
#     tests.append({"G0":10,"Gf":0.1,"T":0.005,"Ep0":0.1,"Epf":1,"P":80})

    # second best param set
#     tests.append({"G0":10,"Gf":0.1,"T":0.005,"Ep0":1,"Epf":1,"P":60})

    # higher PT values were inferior

    plt.figure()
    plt.hold(True)
    for p in problems:
#         plot residual energy vs computation time
#         for each set of params

        sa_energy = []
        sa_time = []
        sa_steps = []
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
            sa_steps.append(steps)
            sa_energy.append(np.mean(energies) - p.exact)
            sa_time.append(1e3*np.mean(times))
#         plt.plot(sa_time, sa_energy, 'o-', markersize=10, label="SA", alpha=0.5)
        plt.plot(sa_steps, sa_energy, 'o-', markersize=10, label="SA", alpha=0.5)

        for t in tests:
            final_dists = np.zeros((N,t['P']))
            qmc_energy = []
            qmc_time = []
            qmc_steps = []
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
                qmc_steps.append(steps)
                qmc_energy.append(np.mean(energies) - p.exact)
                qmc_time.append(1e3*np.mean(times))

                tcounts = counts*N*float(t['P'])/np.sum(counts)
                params = lib_tests.make_param_string(t,s)
                lib_tests.plot_final_slice_histogram(final_dists.flatten(),
                        t['P'],params,filename,ylims=(p.exact*1.1,p.exact*0.5),actuals=(tcounts,e))


            label = "P={0}; T={1}".format(t['P'],t['T'])
#             plt.plot(qmc_time, qmc_energy, 'o-', markersize=10, label=label, alpha=0.5)
            plt.plot(qmc_steps, qmc_energy, 'o-', markersize=10, label=label, alpha=0.5)

    filename = string.join(['images/test_xor_', time.strftime("%Y-%m-%d_%H-%M-%S"), '.svg'], '')

    plt.ylabel('Residual Energy')
    plt.axhline(y=0, linewidth=1,alpha=0.75,color='g')
    plt.yscale('symlog', linthreshy=0.1)
    plt.xscale('symlog', linthreshy=0.1)
    plt.ylim(-1e-2,1e3)
#     plt.xlabel('Computation Time (ms)')
    plt.xlabel('Number of Monte Carlo Steps')
    plt.legend(loc='best')
    plt.title('XOR Gate at Various PT Values')
    plt.grid(True)
    plt.savefig(filename, bbox_inches='tight', format='svg', dpi=1200)
    plt.close()
