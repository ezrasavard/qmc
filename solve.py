#!/usr/bin/python

import argparse
import sys

import ising
import simulated_annealing

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(prog="Ising Solvers")
    subparsers = parser.add_subparsers(help="solver selection")
    
    # parser for config file option
    parser_file = subparsers.add_parser("file", help="read from file")
    parser_file.add_argument("filepath", type=str, help="a file describing all parameters")
    
    # parent parser for solvers
    parser_solver = argparse.ArgumentParser(add_help=False)
    parser_solver.add_argument("-problem", type=str, default="sample_data/ising12.txt", help="a file containing problem data in three column format, see README for details")
    parser_solver.add_argument("-steps", type=int, default=10000, help="number of monte carlo steps (MCS) used, good values depend on problem size")
    parser_solver.add_argument("-dump", type=str, default=None, help="a file to dump move acceptances to, if desired -- slows down performance")
    
    # parser for PI-QMC
    parser_qmc = subparsers.add_parser("qmc", parents=[parser_solver], help="use PI-QMC with commandline arguments")
    parser_qmc.add_argument("-P", type=int, default=40, help="number of trotter slices (replicas), 20 to 80 is typical")
    parser_qmc.add_argument("-T", type=float, default=0.015, help="ambient temperature in K, 0.015 is typical")
    parser_qmc.add_argument("-G0", type=float, default=3, help="initial transverse field strength")
    parser_qmc.add_argument("-Gf", type=float, default=1e-6, help="final tranverse field strength, typically near zero")
    parser_qmc.add_argument("-e0", type=float, default=1e-6, help="initial coupling pre-factor")
    
    # parser for simulated annealing
    parser_sa = subparsers.add_parser("sa", parents=[parser_solver], help="use simulated annealing with commandline arguments")
    parser_sa.add_argument("-T0", type=float, default=3, help="initial temperature in K, 3 to 5 is typical")
    parser_sa.add_argument("-Tf", type=float, default=0.001, help="final temperature in K, typically near zero")
    
    args = parser.parse_args()
    
    problem = ising.SpinGlass(args.problem)
    print vars(args)
    annealer = simulated_annealing.SimulatedAnnealing(problem, vars(args))
    
    E_final, configuration = annealer.solve()
    print problem
    print "Solver Finished!"