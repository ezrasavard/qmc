import copy
import numpy as np

import monte_carlo

class PathIntegralQMC(monte_carlo.MonteCarloSolver):
    """Search for global energy minimum with PI-QMC
    
    Begins with a wide search across several duplicate slices.
    Strong transverse field (Gamma) encourages moves despite fixed temperature.
    As tranverse field weakens, this quantum superposition begins to collapse
    represented by a strengthening interslice coupling J_perp.
    Moves in single slices, and global moves across all slices are attempted
    and a basic Metropolis-Hastings approach is used to evaluate them.
    """
    
    def __init__(self, problem, params):
        
        super(PathIntegralQMC, self).__init__(problem, params)

        self.solver_name = "Path-Integral Quantum Monte Carlo"
        self.P = params['P']
        # effective temperature
        self.PT = self.P*params['T']
        
        # produce schedules
        sched_G = np.linspace(params['G0'], params['Gf'], params['steps'])
        sched_e = np.linspace(params['e0'], params['ef'], params['steps'])
        
        # interslice coupling schedule
        sched_Jp = -0.5*self.PT*np.log(np.tanh(sched_G/(sched_e*self.PT)))
        
        self.schedule = zip(sched_Jp, sched_G)
        
        # copy problem objects into every slice
        # there is some replication of storage here (J matrix, etc.)
        # but it allows using the class methods without passing extra data
        # back and forth
        self.slices = []
        for x in range(self.P):
            self.slices.append(copy.deepcopy(problem))


    def solve(self):
        """Solve the problem and return the solution energy and configuration"""

        if self.outfile:
            fp = open(self.outfile, 'w')
            config = self.p.spins_to_hex() + ",-1"
            fp.write("{}\n{}\n{}\n".format(self.solver_name, self.params, repr(self.p)))
            self._state_dump(fp, self.params["G0"], self.p.E, config)

        for Jp, G in self.schedule:
            # try local moves in all slices, in random order
            slices = np.random.permutation(self.P)
            for k in slices:
                # choose a random spin
                i = np.random.randint(0, self.p.size)
                
                # get local energy cost
                dE = self.slices[k].calculate_dE(i)
                
                # get interslice energy cost
                dE_i = self.calculate_dE_interslice(k, i, Jp)
                if self.step_accepted(dE + dE_i, self.PT):
                    self.slices[k].flip_spin(i)
                    self.slices[k].E += dE
                
                    # this will slow things down quite a bit, but is cool to see
                    if self.outfile:
                        # append the slice number for future use
                        config = self.slices[k].spins_to_hex() + ",{}".format(k)
                        self._state_dump(fp, G, self.slices[k].E, config)
            
            dE_global = np.zeros(self.P)
            # try a global move on a random spin
            # Jp doesn't impact global moves
            i = np.random.randint(0, self.p.size)
            for k in range(self.P):
                dE_global[k] = self.slices[k].calculate_dE(i)
                
            if self.step_accepted(np.sum(dE_global), self.PT):
                for k in range(self.P):
                    self.slices[k].flip_spin(i)
                    self.slices[k].E += dE_global[k]
                    
                    if self.outfile:
                        # append the slice number for future use
                        config = self.slices[k].spins_to_hex() + ",{}".format(k)
                        self._state_dump(fp, G, self.slices[k].E, config)
                
        if self.outfile:
            fp.close()
        
        # Get the best from all slices and store it in the original problem object
        energies = [x.E for x in self.slices]
        best = np.argmin(energies)
        self.p.E = energies[best]
        self.p.spins = self.slices[best].spins.copy()

        return self.p.E, self.p.spins_to_hex()
        
        
    def calculate_dE_interslice(self, k, i, Jp):
        """Calculate the interslice energy of a spin flip and apply periodic
        boundary conditions between replicas
        
        k: the slice index
        i: the spin index
        Jp: the current interslice coupling strength
        """
        
        # dE = -2*spin*Jp(spin_left + spin_right)
        dE = -2*Jp*self.slices[k].get_spin(i)
        
        # find neighbours and apply boundary conditions
        left = k - 1
        right = k + 1 if k + 1 < self.P else 0
        
        return dE*(self.slices[left].get_spin(i) + self.slices[right].get_spin(i))
        
