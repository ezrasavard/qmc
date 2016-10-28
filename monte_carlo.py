import copy
import numpy as np

class MonteCarloSolver(object):
    """Base Class for Markov Chain Monte Carlo Methods"""

    def __init__(self, problem, params, steps=1e5, outfile=None):
        """Basic parameters for a Monte Carlo Solver

        problem: an ising.SpinGlass object.
        steps: number of steps to run for.
        params: dictionary of solver parameters.
        outfile: if defined, solver will dump energy, configurations and
        schedule information into this file.
        """

        self.p = problem
        self.steps = steps
        self.params = copy.deepcopy(params)
        self.outfile = outfile

    
    @staticmethod
    def step_accepted(dE, T, dist=np.random.uniform):
        """Accept or reject a Monte Carlo trial step
        
        Return true if accepting the move
        dE: energy change for the trial step
        T: ambient temperature for evaluation
        dist: distribution to compare against, defaults to uniform
        """

        return (dE <= 0.0 or np.exp(-dE/T) > dist())


    def __repr__(self):

        return '{}(problem={}, steps={}, params={})'.format(self.__class__,
            repr(self.p), self.steps, self.params)