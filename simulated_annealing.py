import numpy as np
from collections import deque

import monte_carlo

class SimulatedAnnealing(monte_carlo.MonteCarloSolver):
    """Search for global energy minimum with Simulated Annealing
    
    Begins with wide search and narrows around minima by lowering temperature,
    leading to a lower probability of accepting a poor move, using a basic
    Metropolis-Hastings approach.
    """
    
    def __init__(self, problem, T0, Tf, steps=1e5):
        
        self.schedule = np.linspace(T0, Tf, steps)
        super(SimulatedAnnealing, self).__init__(problem, steps)

    
    def solve(self):
        """Solve the problem!"""
        
        # store last thousand trials
        energies = deque(maxlen=1000)
        for T in self.schedule:
            # choose a random spin
            i = np.random.randint(0, self.p.size)
            dE = self.p.calculate_dE(i)
            if self.step_accepted(dE, T):
                self.p.spins[i] *= -1
                self.p.E += dE
            energies.append((self.p.E, self.p.spins_to_hex(self.p.spins)))

        # get the best from the last thousand trials
        best = np.amin(energies, axis=0)
        self.p.E = best[0]
        self.p.spins = self.p.hex_to_spins(best[1], self.p.size)