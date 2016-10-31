Path Integral Quantum Monte Carlo (QMC) and Simulated Annealing (SA) for solving
ising spin glasses.

It is free software under the MIT License, and is distributed in the hope 
that it will be useful. See "LICENSE" for details.

# Background
This is a re-write of [my undergraduate research tools](https://github.com/ezrasavard/qmc/tree/undergrad), to be more user-friendly, generally better written, and more useful to someone trying to learn about these algorithms or solving these problems. The solver includes both simulated annealing and PI-QMC.

This newer version is in active development, but is currently functional.

# How to Use
Run solve.py at a terminal and follow the help messages. Default arguments are provided for both solvers and you can override them selectively. In the near future, I'll include a "read from file" capability for parameters.

Output will be printed to the console, including an example string for how to run the same test with the same randomized input, like this:

<pre>
Ising Spin Glass
+----------------+-------------------------------------------------------------------+
| Field          | Value                                                             |
+----------------+-------------------------------------------------------------------+
| data file      | sample_data/ising12.txt                                           |
| description    | random 12x12 spin ising model with solution energy of -18,972,276 |
| initial config | 0xadc82fcf240126042784aabeb7fb762a226b                            |
| current config | 0xb00f9b4fb7732e13ec522859575feb52ba42                            |
| initial energy | -792014.0                                                         |
| current energy | -18018940.0                                                       |
+----------------+-------------------------------------------------------------------+

Solver: Path-Integral Quantum Monte Carlo
+-----------+-------+
| Parameter | Value |
+-----------+-------+
| G0        | 3     |
| Gf        | 1e-06 |
| P         | 40    |
| T         | 0.015 |
| dump      | None  |
| e0        | 1e-06 |
| ef        | 4     |
| steps     | 10000 |
+-----------+-------+
To replicate starting conditions, run with arguments:
        qmc -ef 4 -G0 3 -P 40 -steps 10000 -T 0.015 -problem sample_data/ising12.txt -Gf 1e-06 -e0 1e-06 -spins 0xadc82fcf240126042784aabeb7fb762a226b
</pre>

# Data Input
Problem data is read from a file. The first row of the file contains a description and below that, every row is a set of three values:

    i j J_ij

Where i and j are spin numbers and Jij is the coupling between them. If i and j are equal, then J_ij is the self coupling (h_i). There are example files in sample_data/. Good samples can be obtained from the [spin glass server](http://www.informatik.uni-koeln.de/spinglass/).

# Acknowledgements
Much of the work on path integral quantum monte carlo simulation is based off
the 2003 paper "Quantum Annealing by the path-integral Monte Carlo method..." by
Martonak et al.