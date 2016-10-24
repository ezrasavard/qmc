Path Integral Quantum Monte Carlo (QMC) and Simulated Annealing (SA) for solving
ising spin glasses.

It is free software under the MIT License, and is distributed in the hope 
that it will be useful. See "LICENSE" for details.

#Background
This is a C port and enhancement of my undergrad thesis, doing QMC
in Python. It is not production quality code, but can serve as an example of how to implement these algorithms in two different styles. The Python code uses numpy and matrix operations to perform calculations while the C code uses loops loops and adjacency lists. Both versions include a simulated annealing and PI-QMC implementation.

Problem formats are designed to work with existing code for Quantum-dot
Cellular Automata (QCA).

I have a few features planned for this project in the long run, but it is going
into hibernation.

#Acknowledgements
This research was funded by NSERC and the University of
British Columbia, so thanks for that!

Much of the work on path integral quantum monte carlo simulation is based off
the 2003 paper "Quantum Annealing by the path-integral Monte Carlo method..." by
Martonak et al.

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

	--log_accepts:        turn on logging of move acceptances            

	--log_thresh <float>: threshold for logging slice energies            

	--T <int>:            annealing temp            

Keyworded Aguments (QMC only):            

	--P <int>:            number of trotter slices            

	--PTxJ <double>:      overrides T choice and sets PT as multipler
	                      of the average coupling strength in the problem            

	--MCSxS <int>:        sets the number of monte carlo steps as a 
	                      multiple of the number of spins in the problem            

	--automagic:          (experimental!) automatically choose PTxJ and MCSxS 
	                      to simulate the DWave output distribution            

	--schedule <file>:    file describing annealing schedule            

See "examples" for examples of usage
