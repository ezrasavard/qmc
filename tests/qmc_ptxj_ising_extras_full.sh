#!/bin/bash

# Compare QMC and SA for XOR sweeping Tau
# Compare QMC and SA for Ising32 sweeping Tau

# ising32 QMC PTxJ Sweep
#10

../solve ../data/ising32.txt ../results/qmc_PTxJ_sweep/ising32/qmc_010_2000.txt qmc --trials 100 --P 60 --PTxJ 200 --MCSxS 10;
../solve ../data/ising32.txt ../results/qmc_PTxJ_sweep/ising32/qmc_010_5000.txt qmc --trials 100 --P 60 --PTxJ 500 --MCSxS 10;
../solve ../data/ising32.txt ../results/qmc_PTxJ_sweep/ising32/qmc_010_10000.txt qmc --trials 100 --P 60 --PTxJ 1000 --MCSxS 10;
#100
../solve ../data/ising32.txt ../results/qmc_PTxJ_sweep/ising32/qmc_100_2000.txt qmc --trials 100 --P 60 --PTxJ 200 --MCSxS 100;
../solve ../data/ising32.txt ../results/qmc_PTxJ_sweep/ising32/qmc_100_5000.txt qmc --trials 100 --P 60 --PTxJ 500 --MCSxS 100;
../solve ../data/ising32.txt ../results/qmc_PTxJ_sweep/ising32/qmc_100_10000.txt qmc --trials 100 --P 60 --PTxJ 1000 --MCSxS 100;
#500
../solve ../data/ising32.txt ../results/qmc_PTxJ_sweep/ising32/qmc_500_2000.txt qmc --trials 100 --P 60 --PTxJ 200 --MCSxS 500;
../solve ../data/ising32.txt ../results/qmc_PTxJ_sweep/ising32/qmc_500_5000.txt qmc --trials 100 --P 60 --PTxJ 500 --MCSxS 500;
../solve ../data/ising32.txt ../results/qmc_PTxJ_sweep/ising32/qmc_500_10000.txt qmc --trials 100 --P 60 --PTxJ 1000 --MCSxS 500;
#1000
../solve ../data/ising32.txt ../results/qmc_PTxJ_sweep/ising32/qmc_1e3_2000.txt qmc --trials 100 --P 60 --PTxJ 200 --MCSxS 1000;
../solve ../data/ising32.txt ../results/qmc_PTxJ_sweep/ising32/qmc_1e3_5000.txt qmc --trials 100 --P 60 --PTxJ 500 --MCSxS 1000;
../solve ../data/ising32.txt ../results/qmc_PTxJ_sweep/ising32/qmc_1e3_10000.txt qmc --trials 100 --P 60 --PTxJ 1000 --MCSxS 1000;
#2000
../solve ../data/ising32.txt ../results/qmc_PTxJ_sweep/ising32/qmc_2e3_2000.txt qmc --trials 100 --P 60 --PTxJ 200 --MCSxS 2000;
../solve ../data/ising32.txt ../results/qmc_PTxJ_sweep/ising32/qmc_2e3_5000.txt qmc --trials 100 --P 60 --PTxJ 500 --MCSxS 2000;
../solve ../data/ising32.txt ../results/qmc_PTxJ_sweep/ising32/qmc_2e3_10000.txt qmc --trials 100 --P 60 --PTxJ 1000 --MCSxS 2000;