#!/usr/bin/python

# tests and plots I frequently use

import copy
import matplotlib.pyplot as plt
import numpy as np
import string
import sys
import time

import qmc
import problem

## Plots ##

def plot_QMC_vs_SA_finalE_sweep_Epf(qmc_data, sa_energy, exact, param_string, outfile_slug, ylims=None):
    # qmc_data: qmc final results, Epf
    # sa_energy: sa final results
    # exact: exact solution
    # param_string: string of relevant test parameters for plot title
    # outfile_slug: for outfile name
    # ylims: tuple for plot y-axis limits, if desired for consistency

    filename = string.join(['images/qmc-vs-sa-final-E-Epf-sweep_', outfile_slug,
                           '_', time.strftime("%Y-%m-%d_%H-%M-%S"), '.svg'], '')

    plt.figure()

    e_qmc = qmc_data[1:,0] - exact
    Epfs = qmc_data[1:,1]
    e_sa = sa_energy - exact

    plt.ylabel('Average Residual Energy')
    plt.axhline(y=e_sa,color='r',linestyle='-.',label='SA')
    E = qmc_data[0,0] - exact
    plt.plot(qmc_data[0,1], E, 'x', markersize=10,label="QMC")
    for i, Epf in enumerate(Epfs):
        plt.plot(Epf, e_qmc[i], 'x', markersize=10)
    plt.axhline(y=0, linewidth=1,alpha=0.75,color='g')
    plt.yscale('symlog', linthreshy=0.015)
#     plt.xscale('symlog', linthreshy=0.1)
    if ylims:
        plt.ylim(ylims)
    plt.xlabel('Epsilon Final')
    plt.legend()
    plt.title('QMC vs SA Final Energies Epsilon Sweep'
              '\nTest Parameters:{0}'.format(param_string))
    plt.grid(True)
    plt.savefig(filename, bbox_inches='tight', format='svg', dpi=1200)
    plt.close()


def plot_QMC_vs_SA_finalE_vs_Time(qmc_data, sa_data, exact, param_string, outfile_slug, ylims=None):
    # qmc_data: qmc final results, time
    # sa_data: sa final results, time
    # exact: exact solution
    # param_string: string of relevant test parameters for plot title
    # outfile_slug: for outfile name
    # ylims: tuple for plot y-axis limits, if desired for consistency

    filename = string.join(['images/qmc-vs-sa-final-E_', outfile_slug,
                           '_', time.strftime("%Y-%m-%d_%H-%M-%S"), '.svg'], '')

    plt.figure()
    e_qmc = qmc_data[:,0] - exact
    t_qmc = 1e3*qmc_data[:,1] # in ms
    e_sa = sa_data[:,0] - exact
    t_sa = 1e3*sa_data[:,1] # in ms

    plt.ylabel('Residual Energy')
    plt.plot(t_qmc, e_qmc, 'xk-', alpha=0.75)
    plt.plot(t_qmc, e_qmc, '.b-', alpha=0.75, label='QMC')
    plt.plot(t_sa, e_sa, 'xk-', alpha=0.75)
    plt.plot(t_sa, e_sa, '.r-', alpha=0.75, label='SA')
    plt.axhline(y=0, linewidth=1,alpha=0.75,color='g')
    plt.yscale('symlog', linthreshy=0.015)
    plt.xscale('symlog', linthreshy=0.1)
    if ylims:
        plt.ylim(ylims)
    plt.xlabel('Computation Time (ms)')
    plt.legend()
    plt.title('QMC vs SA Final Energies\
            \nTest Parameters:{0}'.format(param_string))
    plt.grid(True)
    plt.savefig(filename, bbox_inches='tight', format='svg', dpi=1200)
    plt.close()


def plot_QMC_vs_SA_energies(qmc_s, sa_s, t_qmc, t_sa, param_string,
                            outfile_slug, ylims=None):
    # qmc_s: qmc solver instance
    # sa_s: simulated annealing solver instance
    # t_qmc: qmc runtime
    # t_sa: sa runtime
    # param_string: string of relevant test parameters for plot title
    # outfile_slug: for outfile name
    # ylims: tuple for plot y-axis limits, if desired for consistency

    filename = string.join(['images/qmc_vs_sa', '_', outfile_slug,
                           '_', time.strftime("%Y-%m-%d_%H-%M-%S"), '.svg'], '')

    plt.figure()
    e_qmc = qmc_s.data['lowest_energies'] - qmc_s.exact
    e_sa = sa_s.data['lowest_energies'] - qmc_s.exact
    t_qmc = 1e3*np.linspace(0, t_qmc, len(e_qmc))
    t_sa = 1e3*np.linspace(0, t_sa, len(e_sa))


    plt.ylabel('Residual Energy')
    plt.subplot(211)
#     plt.semilogy(t_qmc, e_qmc, linewidth=2, alpha=0.75,color='b',
#             label='QMC')
#     plt.semilogy(t_sa, e_sa, linewidth=2, alpha=0.75,color='r',
#             label='SA')
    plt.plot(t_qmc, e_qmc, linewidth=2, alpha=0.75,color='b',
            label='QMC')
    plt.plot(t_sa, e_sa, linewidth=2, alpha=0.75,color='r',
            label='SA')
    plt.yscale('symlog', linthreshy=0.015)
    if ylims:
        plt.ylim(ylims)
    plt.xlabel('Computation Time (ms)')
    plt.legend()
    plt.title('QMC vs SA\
            \nTest Parameters:{0}'.format(param_string))

    ylims2 = (0.5*min(e_qmc[-1],e_sa[-1]),2*max(e_qmc[-1],e_sa[-1]))
    xlims2 = (0.7*min(t_qmc[-1],t_sa[-1]),max(t_qmc[-1],t_sa[-1]))
    plt.subplot(212)
    plt.hold(True)
#     plt.semilogy(t_sa, e_sa, linewidth=2, alpha=0.75,color='r',
#             label='SA')
#     plt.semilogy(t_qmc, e_qmc, linewidth=2, alpha=0.75,color='b',
#             label='QMC')
    plt.plot(t_sa, e_sa, linewidth=2, alpha=0.75,color='r',
            label='SA')
    plt.plot(t_qmc, e_qmc, linewidth=2, alpha=0.75,color='b',
            label='QMC')
    plt.yscale('symlog', linthreshy=0.015)
    plt.xlim(xlims2)
    plt.ylim(ylims2)
    plt.grid(True)
    plt.savefig(filename, bbox_inches='tight', format='svg', dpi=1200)
    plt.close()


def plot_energies(s, param_string, outfile_slug, ylims=None):
    # s: solver instance
    # param_string: string of relevant test parameters for plot title
    # outfile_slug: for outfile name
    # ylims: tuple for plot y-axis limits, if desired for consistency


    filename = string.join(['images/energies', '_', outfile_slug,
                           '_', time.strftime("%Y-%m-%d_%H-%M-%S"), '.svg'], '')

    plt.figure()
    if s.exact:
        plt.axhline(y=s.exact, linewidth=1,alpha=0.75,color='g',label='Exact Solution')
        if not ylims:
            ylims = (s.exact*1.1, s.exact*0.4)
    energies = s.data['lowest_energies']
    plt.plot(s.Tau, energies, linewidth=2, alpha=0.75,color='b',
            label='Min Slice Energy')
    plt.xlabel('Tau (MCS)')
    plt.ylabel('Min Slice Energy')
    if ylims:
        plt.ylim(ylims)
    plt.legend()
    plt.title('Minimum Slice Energy During QA\
            \nTest Parameters:{0}'.format(param_string))
    plt.grid(True)
    plt.savefig(filename, bbox_inches='tight', format='svg', dpi=1200)
    plt.close()


def plot_all_slice_energies(s, param_string, outfile_slug, ylims=None):
    # s: solver instance
    # param_string: string of relevant test parameters for plot title
    # outfile_slug: for outfile name
    # ylims: tuple for plot y-axis limits, if desired for consistency

    filename = string.join(['images/slice-energies', '_', outfile_slug,
                           '_', time.strftime("%Y-%m-%d_%H-%M-%S"), '.svg'], '')

    plt.figure()
    if s.exact:
        plt.axhline(y=s.exact, linewidth=1,alpha=0.75,color='g',label='Exact Solution')
        if not ylims:
            ylims = (s.exact*1.1, s.exact*0.4)
    for energy in s.data['energy_slices']:
        plt.plot(s.Tau, energy, linewidth=2, alpha=0.75)
    plt.xlabel('Tau (MCS)')
    plt.ylabel('Slice Energies')
    if ylims:
        plt.ylim(ylims)
    plt.legend()
    plt.title('Slice Energies During QA\
            \nTest Parameters:{0}'.format(param_string))
    plt.grid(True)
    plt.savefig(filename, bbox_inches='tight', format='svg', dpi=1200)
    plt.close()


def plot_schedules(s, param_string, outfile_slug, ylims=None):
    # s: solver instance
    # param_string: string of relevant test parameters for plot title
    # outfile_slug: for outfile name
    # ylims: tuple for plot y-axis limits

    filename = string.join(['images/schedule', '_', outfile_slug,
                           '_', time.strftime("%Y-%m-%d_%H-%M-%S"), '.svg'], '')

    plt.figure()
    schedule = np.array(s.schedule)
    plt.plot(s.Tau, schedule[:,0], linewidth=2, alpha=0.75, color='k',
            label='Tranverse Field')
    plt.plot(s.Tau, schedule[:,1], linewidth=2, alpha=0.75, color='y',
            label='Epsilon')
    plt.plot(s.Tau, schedule[:,2], linewidth=2, alpha=0.75, color='r',
            label='Interslice Coupling')
    plt.xlabel('Tau (MCS)')
    plt.ylabel('Field Strength')
    plt.legend()
    plt.grid(True)
    plt.title('Slice Energies During QA\
            \nTest Parameters:{0}'.format(param_string))
    if not ylims:
        ylims = (0, max(schedule[0,0], schedule[-1,1]))
    plt.ylim(ylims)
    plt.savefig(filename, bbox_inches='tight', format='svg', dpi=1200)
    plt.close()


def plot_final_slice_histogram(data, P, param_string, outfile_slug, ylims=None, actuals=None):
    # data: slice energies
    # P: number of slices
    # param_string: string of relevant test parameters for plot title
    # outfile_slug: for outfile name
    # ylims: tuple for plot y-axis limits

    filename = string.join(['images/final_slice_histogram', '_', outfile_slug,
                           '_', time.strftime("%Y-%m-%d_%H-%M-%S"), '.svg'], '')

    plt.figure()
    ylabel = 'Energy'
#     n, bins, patches = plt.hist(data, P, normed=True,
#             orientation='horizontal',facecolor='green', alpha=0.75)
    n, bins, patches = plt.hist(data, P, normed=False,
            orientation='horizontal',facecolor='green', alpha=0.85, label='QMC')
    if actuals:
        plt.legend(loc='best')
        w = 0.2
        plt.barh(actuals[1],actuals[0],w,align='center',color='r',edgecolor='r',alpha=0.4,label="DWave Results")
    plt.ylabel(ylabel)
    plt.xlabel('Slices in State')
    if ylims:
        plt.ylim(ylims)
    plt.xlim((0,len(data)))
    plt.title('Final State Energies of all Slices\
            \nTest Parameters:{0}'.format(param_string))
    plt.grid(True)
    plt.savefig(filename, bbox_inches='tight', format='svg', dpi=1200)
    plt.close()


## Helpers ##

def print_outputs(s, param_string, header, pols=True):
    # header: a string for output header
    # param_string: string of relevant test parameters for plot title

    print "\n------------------------------\n{0}".format(header)
    print "Initial energy: {:.2f}".format(s.initial_energy)
    print "Test Parameters:{0}".format(param_string)
    if pols:
        print "Final polarizations: {0}".format(s.polarizations)
    print "------------------------------\n"


def make_param_string(params, s=None, extra=None):
    # params: a dictionary of parameter names and values for tests
    # s: solver object
    # extra: extra text to include, appended to string

    pstring = ''
    for k,v in params.iteritems():
        tmp = ' ' + k + ': ' + str(v) + ';'
        pstring += tmp
    if s:
        pstring += '\nFinal Energy: ' + '{:.2f}; Exact: {:.2f}'.format(s.final_energy, s.exact)
    if extra:
        pstring += extra

    return pstring


## Tests ##

def QMC_vs_SA_real_time(prob, t, exact, filename):
    # prob: ising problem
    # t: test parameter dictionary
    # exact: exact solution to the problem
    # filename: used in forming name of outfile for plot

    # SA vs QMC
    qmc_s = qmc.PIMC(prob,P=t['P'],G0=t['G0'],Gf=t['Gf'],T=t['T'], Epf=t['Epf'],steps=t['steps'])
    qmc_s.exact = exact
    sa_s = qmc.SimulatedAnnealing(prob,T0=t['T0'],T=1e-4,steps=1.5*t['steps'])

    # time QMC
    t0 = time.time()
    qmc_s.solve()
    tf = time.time()
    t_qmc = tf-t0
    print('QMC time: {:.4f}'.format(t_qmc))

    sa_s.anneal()
    tf2 = time.time()
    t_sa = tf2 - tf
    print('SA time: {:.4f}'.format(t_sa))

    results = '\nQMC Energy: {:.2f}; SA Energy: {:.2f}'.format(qmc_s.final_energy,sa_s.final_energy)

    params = make_param_string(t,extra=results)
    plot_QMC_vs_SA_energies(qmc_s, sa_s, t_qmc, t_sa, params, filename, ylims=(1e-2,1e3))

def QMC_vs_SA_sweep_steps(prob, test_params, exact, filename):
    # prob: ising problem
    # test_params: test parameter dictionary
    # exact: exact solution to the problem
    # filename: used in forming name of outfile for plot

    # SA vs QMC
    tests = [1e2, 1e3, 1e4, 1e5, 1e6, 1e7]
    SA_tests = [1e2, 1e3, 1e4, 1e5, 1e6]
    N = 10 # number of iterations

    t = copy.copy(test_params)
    qmc_data = np.zeros((len(tests),2))
    sa_data = np.zeros((len(tests),2))
    _ = t.pop('steps')
    for i, steps in enumerate(SA_tests):
        energies = []
        times = []
        for k in range(N):
            sa_s = qmc.SimulatedAnnealing(prob,T0=t['T0'],T=1e-4,steps=steps)
            t1 = time.time()
            sa_s.anneal()
            t2 = time.time()
            t_sa = t2 - t1
            print('SA time: {:.4f}'.format(t_sa))
            energies.append(sa_s.final_energy)
            times.append(t_sa)
        sa_energy = np.mean(energies)
        sa_time = np.mean(times)
        sa_data[i] = [sa_energy, sa_time]

    for i, steps in enumerate(tests):
        energies = []
        times = []
        for k in range(N):
            qmc_s = qmc.PIMC(prob,P=t['P'],G0=t['G0'],Gf=t['Gf'],T=t['T'], Epf=t['Epf'],steps=steps)
            qmc_s.exact = exact

            # time QMC
            t1 = time.time()
            qmc_s.solve()
            t2 = time.time()
            t_qmc = t2 - t1
            print('QMC time: {:.4f}'.format(t_qmc))
            energies.append(qmc_s.final_energy)
            times.append(t_qmc)
        qmc_energy = np.mean(energies)
        qmc_time = np.mean(times)
        qmc_data[i] = [qmc_energy, qmc_time]

        results = '\nQMC Energy: {:.2f}; SA Energy: {:.2f}'.format(qmc_s.final_energy,sa_s.final_energy)

        params = make_param_string(t,extra=results)

    print qmc_data

    plot_QMC_vs_SA_finalE_vs_Time(qmc_data, sa_data, exact, params, filename, ylims=(-1e-2,1e3))



def QMC_vs_SA_sweep_Epf(prob, test_params, exact, filename):
    # prob: ising problem
    # test_params: test parameter dictionary
    # exact: exact solution to the problem
    # filename: used in forming name of outfile for plot

    # SA vs QMC
    tests = [1, 4, 8, 16, 32] # Epf values to sweep
    N = 10 # number of runs at each value

    qmc_data = np.zeros((len(tests),2))
    t = copy.copy(test_params)
    _ = t.pop('Epf')

    energies = []
    for k in range(N):
        sa_s = qmc.SimulatedAnnealing(prob,T0=t['T0'],T=1e-4,steps=1.5*t['steps'])
        sa_s.anneal()
        energies.append(sa_s.final_energy)

    sa_energy = np.mean(energies)
    
    print('SA average energy: {:.4f}'.format(sa_energy))

    for i, Epf in enumerate(tests):
        qmc_data[i,1] = Epf
        energies = []

        for k in range(N):
            qmc_s = qmc.PIMC(prob,P=t['P'],G0=t['G0'],Gf=t['Gf'],T=t['T'], Epf=Epf,steps=t['steps'])
            qmc_s.exact = exact
            qmc_s.solve()
            energies.append(qmc_s.final_energy)

        qmc_data[i,0] += np.mean(energies)

    params = make_param_string(t)

    print qmc_data
    plot_QMC_vs_SA_finalE_sweep_Epf(qmc_data, sa_energy, exact, params, filename, ylims=(-1e-2,1e4))


def QMC_real_time_sweep_params(p, filename, steps):
    # p: problem instance

    test_params = []
    test_params.append({"G0":10,"Gf":0.1,"T":0.015,"Epf":1,"Ep0":0.1,"steps":steps,"P":20})
    test_params.append({"G0":10,"Gf":0.1,"T":0.010,"Epf":1,"Ep0":0.1,"steps":steps,"P":30})
    test_params.append({"G0":10,"Gf":0.1,"T":0.0075,"Epf":1,"Ep0":0.1,"steps":steps,"P":40})

    for t in test_params:
        s = qmc.PIMC(p,P=t['P'],G0=t['G0'],Gf=t['Gf'],T=t['T'], Epf=t['Epf'],Ep0=t['Ep0'],steps=t['steps'])
        s.solve()
        params = make_param_string(t, s)
        if p.poles:
            params += '\nPoles: ' + str(p.poles)
        print_outputs(s, params, 'Solution for: {}'.format(filename))
        plot_energies(s, params, filename)
        plot_schedules(s, params, filename)
        try:
            plot_all_slice_energies(s, params, filename)
        except Exception as e:
            print e
            print "could not plot all slice energies"
        plot_final_slice_histogram(s.data['final_slice_energies'], s.P, params, filename)

def QMC_final_distributions(prob, t, filename, N=10):

    energies = np.zeros((N,t['P']))
    for k in range(N):
        s = qmc.PIMC(prob,P=t['P'],G0=t['G0'],Gf=t['Gf'],T=t['T'], Epf=t['Epf'],steps=t['steps'])
        s.solve()
        energies[k,:] = s.data['final_slice_energies']

    params = make_param_string(t, s)
    params += '\nPoles: ' + str(prob.poles)
    data = energies.flatten()
    plot_final_slice_histogram(data, s.P, params, filename)
