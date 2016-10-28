import numpy as np

class MonteCarloSolver(object):
    """Base Class for Markov Chain Monte Carlo Methods"""
    
    def __init__(self, problem, steps=1e5):
        """Basic parameters for a Monte Carlo Solver
        
        problem: an ising.SpinGlass object
        steps: number of steps to run for
        """
        
        self.p = problem
        self.steps = steps
        
    
    @staticmethod
    def step_accepted(dE, T, dist=np.random.uniform):
        """Accept or reject a Monte Carlo trial step
        
        Return true if accepting the move
        dE: energy change for the trial step
        T: ambient temperature for evaluation
        dist: distribution to compare against, defaults to uniform
        """

        return (dE <= 0.0 or np.exp(-dE/T) > dist())