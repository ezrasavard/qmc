Path Integral Quantum Monte Carlo (QMC) and Simulated Annealing (SA) for solving
ising spin glasses.

This file is part of FreePIMC.

FreePIMC is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

FreePIMC is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with FreePIMC.  If not, see <http://www.gnu.org/licenses/>.

#Background
FreePIMC is a C port and enhancement of my undergrad thesis, doing QMC
in Python.

Problem formats are designed to work with existing code for Quantum-dot
Cellular Automata (QCA). Code is being designed to integrate with QCADesigner.

I have a few features planned for this project in the long run, but it is going
into hibernation.

#Acknowledgements
This research was funded by NSERC and the University of
British Columbia, so thanks for that!

Much of the work on path integral quantum monte carlo simulation is based off
the 2003 paper "" by Martonak et al.

#Directory Structure
data:
    files for problems
    files for dwave output data (mostly private, sorry)

examples:
    usage examples for QMC and SA
    example problem data
    example output files

results:
    output files from simulations and analysis
    some pretty plots

scripts:
    scripts for analyzing results and plotting

src:
    source code

tests:
    scripts for running (and generating) tests

#How to Use
Problems should be defined in a three column text file

    cell_id1 cell_id2 coupling

The first line of the file is skipped.
The program expects the couplings as floating point numbers and will scale them
up by a factor of 1e5 and operate on them as long integers.

##--help dump
*** MCMC Solver ***
Program is designed primarily for research using quantum monte carlo

Positional Arguments:            

	problem data file name            
	output file name            
	solver name ('qmc' or 'sa')            
	(DEPRECATED) number of monte carlo steps            
	(DEPRECATED) number of trials            

Keyworded Arguments:            

	--steps <int>:        number of steps to use            

	--trials <int>:       number of trials            

	--P <int>:            number of slices to use in QMC            

	--T <int>:            annealing temp            

	--PTxJ <double>:      overrides T choice and sets PT as multipler
	                      of the average coupling strength in the problem            

	--MCSxS <int>:        sets the number of monte carlo steps as a 
	                      multiple of the number of spins in the problem            

	--log_accepts:        turn on logging of move acceptances in QMC            

	--log_thresh <float>: threshold for logging slice energies in QMC            

See "examples" for examples of usage
