#!/usr/bin/python

import argparse

import ising
import simulated_annealing

if __name__ == "__main__":
    problem = ising.SpinGlass()
    args = {}
    args["T0"] = 3
    args["Tf"] = .015
    annealer = simulated_annealing.SimulatedAnnealing(problem, args, 1e5, "dump.txt")
    
    E_final, configuration = annealer.solve()
    print problem
    print "Solver Finished!"