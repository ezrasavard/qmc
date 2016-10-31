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
    
    def __init__(self, problem, params):
        
        super(SimulatedAnnealing, self).__init__(problem, params)
        self.schedule = np.linspace(params['T0'], params['Tf'], params['steps'])
        # store last thousand trials in queues
        self.queue_len = 1000
        self.energies = deque(maxlen=self.queue_len)
        self.configurations = deque(maxlen=self.queue_len)
        self.solver_name = "Simulated Annealing"

        # write a header
        if self.outfile:
            with open(self.outfile, 'w') as fp:
                fp.write("{}, {}".format(self, datetime.datetime.now()))
                fp.write("T,E,config\n")

    def solve(self):
        """Solve the problem and return the solution energy and configuration"""
        
        storage_thresh = self.steps - self.queue_len
        self.energies.clear()
        self.configurations.clear()

        if self.outfile:
            fp = open(self.outfile, 'w')
            config = self.p.spins_to_hex()
            fp.write("{}\n{}\n{}\n".format(self.solver_name, self.params, repr(self.p)))
            self._state_dump(fp, self.params["T0"], self.p.E, config)

        for step, T in enumerate(self.schedule):
            # choose a random spin
            i = np.random.randint(0, self.p.size)
            dE = self.p.calculate_dE(i)
            if self.step_accepted(dE, T):
                self.p.flip_spin(i)
                self.p.E += dE
                
                # this will slow things down quite a bit, but is cool to see
                if self.outfile:
                    self._state_dump(fp, T, self.p.E, self.p.spins_to_hex())
                    
            
            # store final self.queue_len steps
            if step >= storage_thresh:
                config = self.p.spins_to_hex(self.p.spins)
                self.energies.append(self.p.E)
                self.configurations.append(config)
                
        if self.outfile:
            fp.close()
        
        # Get the best from the queue
        best = np.argmin(self.energies)
        self.p.E = self.energies[best]
        self.p.spins = self.p.hex_to_spins(self.configurations[best])

        return self.p.E, self.configurations[best]
        