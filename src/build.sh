#!/bin/bash

gcc -std=gnu99 -o ../solve main.c mcmc.c ising.c qmc.c -lm -ljansson -gstabs
