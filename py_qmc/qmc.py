#!/usr/bin/python

# Start with an arbitrary quantum Ising Hamiltonian in d dimensions
# Break up H into P d+1 dimensional classical Hamiltonians
# J couples pairs of spins in the same slice
# J_perp couples pairs of the same spin from neighbouring slices
# Slices "wrap around" and have periodic boundary conditions
# J_perp is a function of Gamma, P and T

import copy
import numpy as np
import time

from collections import deque

class MCMC(object):

    def __init__(self, problem, steps=1e5):

        self.problem = problem
        self.spins = copy.copy(problem.spins)
        self.initial_energy = problem.initial_energy
        self.final_energy = None
        self.exact = problem.exact
        self.data = {}
        self.steps = steps
        self.J_symm = problem.J + np.transpose(problem.J)


    def MCS_accepted(self, delta_E, T):
        # accept or reject the Monte Carlo step
        # E: total energy of trial configuration
        # T: ambient temperature

        # evaluate acceptance of move
        if delta_E <= 0.0:
            return True
        elif np.exp(-delta_E/T) > np.random.uniform():
            return True
        else:
            return False

# Hamiltonian (d+1) takes the form:
# H = -\epsilon \sum_{P}^{k} \left( \sum_{i<j} J_{ij} s_i s_j + \sum_{i} h_i s_i + J_{\perp}\sum_{i} s_i^k s_{i}^{k+1} \right)

class PIMC(MCMC):

    def __init__(self, problem, P=40, T=.010, G0=2.5, Ep0=1,
            steps=1e6, outfile=None, Gf=1e-3, Epf=1, update_period=100):
        # problem - ising problem instance
        # P - number of Trotter slices
        # T - ambient temperature for quantum annealing
        # G0 - initial tranverse field
        # Ep0 - coupling scaling parameter
        # steps - size of schedule arrays
        # outfile - file to write data to
        # Gf - final tranverse field
        # Ep0 - final coupling scaling parameter
        # update_period - number of MCS to run between plot data samples

        super(PIMC, self).__init__(problem, steps)

        # prepare path integral parameters
        self.P = P
        self.T = T
        self.slices = np.zeros((P,problem.N),dtype=int)
        self.G0 = G0
        self.Ep0 = Ep0
        self.Epf = Epf

        # copy spin configuration into every slice
        for k in range(P):
            self.slices[k] = copy.copy(problem.spins)

        # schedules
        print "Preparing annealing schedules"
        self.Tau = np.linspace(0,steps,steps)
        G_sched = np.linspace(G0, Gf, steps)
        Ep_sched = np.linspace(Ep0, Epf, steps)
        J_perp = -.5*P*T*np.log(np.tanh(G_sched/(Ep_sched*P*T)))
        self.schedule = zip(G_sched, Ep_sched, J_perp)

        # periodic boundary conditions
        # can use boundary_slices[k] and [k+2] to get neighbouring slices
        boundary_slices = np.linspace(-1,P,P+2)
        boundary_slices[0] = P-1
        boundary_slices[P+1] = 0
        self.boundary_slices = boundary_slices

        # extra stuff for plots
        self.data['lowest_energies'] = np.zeros(steps)
        self.data['energy_slices'] = None
        self.update_period = update_period
        self.data['final_slice_energies'] = []
        self.data['best_GS_configuration'] = []


    def solve(self):

        print "Beginning quantum annealing"
        slice_energies = self.QA()
        self.data['energy_slices'] = slice_energies
        self.data['lowest_energies'] = np.min(slice_energies,0)

        # extract final slice energies
        final_energies = slice_energies[:,-1]
        self.data['final_slice_energies'] = final_energies
        self.data['best_GS_configuration'] = self.slices[np.argmin(final_energies)]
        self.final_energy = np.amin(final_energies)
        self.polarizations = self.calc_polarizations(final_energies)


    def calc_polarizations(self, slice_energies):
        # calculate a Boltzmann weighted polarization from
        # slice configurations and respective energies
        # the result is a single row array of QCA cell polarizations
        # FIXME: have not verified that this makes any sense!

        x = np.exp(-slice_energies/np.max(slice_energies))
        boltz = x/np.sum(x)
        return np.dot(boltz, self.slices)


    def QA(self):
        # Quantum annealing process
        period = float(self.update_period)
        slice_local_energies = self.get_slice_energies()
        energy_slices = np.zeros((self.P, self.steps))
        for tau, (G, Ep, J_perp) in enumerate(self.schedule, 1):
            # P local moves
            slice_indices = np.random.permutation(self.P)
            for k in slice_indices:
                spins = self.slices[k]
                i = np.random.randint(self.problem.N) # random spin
                dE_slice = self.get_delta_E_slice(i, k)
                dE_inter = self.get_delta_E_inter(i, k, J_perp)
                delta_E = Ep*(dE_slice+dE_inter)
                if self.MCS_accepted(delta_E, self.T*self.P):
                    spins[i] *= -1
                    slice_local_energies[k] += dE_slice

            # one global move
            i = np.random.randint(self.problem.N) # random spin
            delta_E_slices = self.get_delta_slice_energies(i)
            delta_E = np.sum(delta_E_slices)*Ep
            if self.MCS_accepted(delta_E, self.T*self.P):
                self.slices[:,i] *= -1
                slice_local_energies += delta_E_slices

            energy_slices[:,tau-1] = slice_local_energies[:]

        return energy_slices


    def get_slice_energies(self, J_perp=None):
        # return list of slice energies
        # local: disregard interslice coupling

        # self couplings
        E_array = np.dot(self.slices, self.problem.h)

        # slice local couplings
        x = np.dot(self.slices, self.problem.J)
        E_array += np.sum(x*self.slices,1)
        if J_perp:
            x = np.roll(self.slices,1,0)*self.slices
            E_interslice = J_perp*np.sum(x,1)
            E_array += E_interslice

        return E_array


    def get_slice_local_energy(self, i, k):

        # self coupling
        E = self.slices[k,i]*self.problem.h[i]

        # slice local
        couplings = np.sum(np.dot(self.slices[k], self.J_symm[:,i]))
        E += couplings*self.slices[k,i]

        return E


    def get_interslice_energy(self, i, k, J_perp):

        left = self.boundary_slices[k]
        right = self.boundary_slices[k+2]
        coupling = self.slices[k,i]*(self.slices[left,i] + self.slices[right,i])
        E = J_perp*coupling

        return E
        
    def get_delta_E_slice(self, i, k):
        '''Change in slice energy due to flipping spin i in slice k'''
        
        E = self.problem.h[i] + np.dot(self.slices[k, :], self.J_symm[:, i])
        return -2*self.slices[k,i]*E
        
    def get_delta_E_inter(self, i, k, J_perp):
        '''Change in inter-slice energy due to flipping spin i in slice k'''
        
        left = self.boundary_slices[k]
        right = self.boundary_slices[k+2]
        E = self.slices[left,i] + self.slices[right,i]
        return -2*self.slices[k,i]*J_perp*E
    
    def get_delta_slice_energies(self, i):
        '''Change in total energy due to flipping spin i in all slices'''
        
        e_locs = self.problem.h[i] + np.dot(self.slices, self.J_symm[:, i])
        E = np.multiply(self.slices[:, i], e_locs)
        return -2*E

class SimulatedAnnealing(MCMC):

    def __init__(self, problem, T0, T, steps=1e6):

        super(SimulatedAnnealing, self).__init__(problem, steps)
        self.schedule = np.linspace(T0, T, self.steps)

    def get_spin_energy(self, i):

        # self coupling
        E = self.spins[i]*self.problem.h[i]

        # slice local
        couplings = np.sum(np.dot(self.spins, self.J_symm[:,i]))
        E += couplings*self.spins[i]

        return E

    def get_delta_E(self, i):
        E = self.problem.h[i]+ np.dot(self.spins, self.J_symm[:, i])
        return -2*self.spins[i]*E

    def anneal(self):

        # this is really slow, and I don't understand why
        # I thought it used to be really fast.
        energies = deque(maxlen=1000)
        E = self.initial_energy
        print "Beginning classical simulated annealing"
        for step, T in enumerate(self.schedule, 1):
            i = np.random.randint(0,self.problem.N)
            delta_E = self.get_delta_E(i)
            if self.MCS_accepted(delta_E, T):
                self.spins[i] *= -1
                E += delta_E
            energies.append(E)

        self.final_energy = np.min(E)
