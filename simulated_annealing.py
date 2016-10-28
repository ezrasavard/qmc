import datetime
import numpy as np
from collections import deque

import monte_carlo

class SimulatedAnnealing(monte_carlo.MonteCarloSolver):
    """Search for global energy minimum with Simulated Annealing
    
    Begins with wide search and narrows around minima by lowering temperature,
    leading to a lower probability of accepting a poor move, using a basic
    Metropolis-Hastings approach.
    """
    
    def __init__(self, problem, params, steps=1e5, outfile=None):
        
        super(SimulatedAnnealing, self).__init__(problem, steps, params, outfile)
        self.schedule = np.linspace(self.params['T0'], self.params['Tf'], steps)
        # store last thousand trials in a queue
        self.results = deque(maxlen=1000)
        
        # write a header
        if self.outfile:
            with open(self.outfile, 'w') as fp:
                fp.write("{}, {}".format(self, datetime.datetime()))
                fp.write("T,E,config\n")

    def solve(self):
        """Solve the problem and return the solution energy and configuration"""
        
        self.results.clear()
        if self.outfile:
            fp = open(self.outfile, 'w')
            
        for T in self.schedule:
            # choose a random spin
            i = np.random.randint(0, self.p.size)
            dE = self.p.calculate_dE(i)
            if self.step_accepted(dE, T):
                self.p.spins[i] *= -1
                self.p.E += dE
            config = self.p.spins_to_hex(self.p.spins)
            self.results.append((self.p.E, config))
            if self.outfile:
                fp.write(self._state_dump(T, self.p.E, config))
            
        if self.outfile:
            fp.close()
            
        return self.getResults()

    def _state_dump(self, sched, E, configuration):
        
        return "{},{},{}\n".format(" ".join(sched), E, configuration)

    def getResults(self):
        """Get the best from the queue"""
        
        best = np.amin(self.results, axis=0)
        self.p.E = best[0]
        self.p.spins = self.p.hex_to_spins(best[1], self.p.size)