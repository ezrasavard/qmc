#!/usr/bin/python

# a file for calling my tests

import copy
import numpy as np
import string
import sys
import time

import lib_tests
import matplotlib.pyplot as plt
import problem
import qca_embed.new_src.qca_solver as qca
import qca_embed.new_src.solvers.rp_solve as rp
import qmc


if __name__=="__main__":

    wires = []
    wires.append('primitives/wire/wire-10.qca')
    wires.append('primitives/wire/wire-20.qca')
    wires.append('primitives/wire/wire-30.qca')
    wires.append('primitives/wire/wire-50.qca')

    problems = []
    for data_file in wires:
        filename = data_file.split('/')[-1]
        tmp = filename.split('.')
        filename = tmp[-2]
        h_list, J_n, poles = qca.exact_solve(data_file, ret=True, do_solve=False)
        h = h_list[0]
        p = problem.ising(hJ=(h,J_n), fname=filename)
        exacts, soln_vects, modes = rp.rp_solve(h, J_n, 0.1)
        p.exact = float(exacts[0])
        p.initial_energy = p.get_E()
        print p.filename
        print p.initial_energy
        print p.exact
        problems.append(p)

    steps_list = [1e3, 5e3, 1e4, 5e4, 1e5]

    plt.figure()
    plt.hold(True)
    for p in problems:
#         plot residual energy vs computation time
#         for each length of wire
#         SA would clutter things up, so ignore it

        qmc_energy = []
        qmc_time = []
        qmc_steps = []
        for steps in steps_list:
            t = {"G0":10,"Gf":0.1,"T":0.005,"Ep0":0.1,"Epf":1,"P":60}
            N = 5
            energies = []
            times = []
            for k in range(N):
                s = qmc.PIMC(p,P=t['P'],G0=t['G0'],Gf=t['Gf'],T=t['T'],Epf=t['Epf'],steps=steps)

                # time QMC
                t1 = time.time()
                s.solve()
                t2 = time.time()
                t_qmc = t2 - t1
                print('QMC time: {:.4f}'.format(t_qmc))
                energies.append(s.final_energy)
                times.append(t_qmc)
            qmc_energy.append(np.mean(energies) - p.exact)
            qmc_time.append(1e3*np.mean(times))
            qmc_steps.append(steps)
        plt.plot(qmc_steps, qmc_energy, 'o-', markersize=10, label=p.filename, alpha=0.5)

    params = lib_tests.make_param_string(t)
    filename = string.join(['images/wires_', time.strftime("%Y-%m-%d_%H-%M-%S"), '.svg'], '')

    plt.ylabel('Residual Energy')
    plt.axhline(y=0, linewidth=1,alpha=0.75,color='g')
    plt.yscale('symlog', linthreshy=0.015)
    plt.xscale('symlog', linthreshy=0.1)
    plt.ylim(-1e-2,1e3)
    plt.xlabel('Monte Carlo Steps')
    plt.legend(loc='best')
    plt.title('QMC Scaling with Wires\
            \nTest Parameters:{0}'.format(params))
    plt.grid(True)
    plt.savefig(filename, bbox_inches='tight', format='svg', dpi=1200)
    plt.close()
