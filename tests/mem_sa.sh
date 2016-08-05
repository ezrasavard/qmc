#!/bin/bash

#SA
../solve ../data/mem100/sol0.txt ../results/qmc_PTxJ_sweep/mem/sa010.txt sa --trials 100 --MCSxS 10;
../solve ../data/mem100/sol0.txt ../results/qmc_PTxJ_sweep/mem/sa100.txt sa --trials 100 --MCSxS 100;
../solve ../data/mem100/sol0.txt ../results/qmc_PTxJ_sweep/mem/sa500.txt sa --trials 100 --MCSxS 500;
../solve ../data/mem100/sol0.txt ../results/qmc_PTxJ_sweep/mem/sa1e3.txt sa --trials 100 --MCSxS 1000;
../solve ../data/mem100/sol0.txt ../results/qmc_PTxJ_sweep/mem/sa2e3.txt sa --trials 100 --MCSxS 2000;