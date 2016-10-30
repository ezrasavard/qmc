#!/usr/bin/python

import argparse
import sys

import ising
import simulated_annealing

if __name__ == "__main__":
    problem = ising.SpinGlass(sys.argv[1])
    args = {}
    args["T0"] = 3
    args["Tf"] = .01
    annealer = simulated_annealing.SimulatedAnnealing(problem, args, 1e4, "dump.txt")
    
    E_final, configuration = annealer.solve()
    print problem
    print "Solver Finished!"