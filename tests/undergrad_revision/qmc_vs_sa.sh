#!/bin/bash

# Compare QMC and SA for XOR sweeping Tau
# Compare QMC and SA for Ising32 sweeping Tau
# Small sweep of PT for XOR, compare each PT along with SA.

# Replace simulation plots with "not good" ones from recent batch of XOR and something else, not MAJ.

# XOR QMC
../solve ../data/xor100/sol0.txt ../results/qmc_vs_sa/xor/qmc010.txt qmc --trials 100 --P 60 --PTxJ 25 --MCSxS 10;
../solve ../data/xor100/sol0.txt ../results/qmc_vs_sa/xor/qmc100.txt qmc --trials 100 --P 60 --PTxJ 25 --MCSxS 100;
../solve ../data/xor100/sol0.txt ../results/qmc_vs_sa/xor/qmc500.txt qmc --trials 100 --P 60 --PTxJ 25 --MCSxS 500;
../solve ../data/xor100/sol0.txt ../results/qmc_vs_sa/xor/qmc1e3.txt qmc --trials 100 --P 60 --PTxJ 25 --MCSxS 1000;
../solve ../data/xor100/sol0.txt ../results/qmc_vs_sa/xor/qmc2e3.txt qmc --trials 100 --P 60 --PTxJ 25 --MCSxS 2000;

# XOR SA
../solve ../data/xor100/sol0.txt ../results/qmc_vs_sa/xor/sa010.txt sa --trials 100 --MCSxS 10;
../solve ../data/xor100/sol0.txt ../results/qmc_vs_sa/xor/sa100.txt sa --trials 100 --MCSxS 100;
../solve ../data/xor100/sol0.txt ../results/qmc_vs_sa/xor/sa500.txt sa --trials 100 --MCSxS 500;
../solve ../data/xor100/sol0.txt ../results/qmc_vs_sa/xor/sa1e3.txt sa --trials 100 --MCSxS 1000;
../solve ../data/xor100/sol0.txt ../results/qmc_vs_sa/xor/sa2e3.txt sa --trials 100 --MCSxS 2000;

# ising32 QMC
../solve ../data/ising32.txt ../results/qmc_vs_sa/ising32/qmc010.txt qmc --trials 100 --P 60 --PTxJ 25 --MCSxS 10;
../solve ../data/ising32.txt ../results/qmc_vs_sa/ising32/qmc100.txt qmc --trials 100 --P 60 --PTxJ 25 --MCSxS 100;
../solve ../data/ising32.txt ../results/qmc_vs_sa/ising32/qmc500.txt qmc --trials 100 --P 60 --PTxJ 25 --MCSxS 500;
../solve ../data/ising32.txt ../results/qmc_vs_sa/ising32/qmc1e3.txt qmc --trials 100 --P 60 --PTxJ 25 --MCSxS 1000;
../solve ../data/ising32.txt ../results/qmc_vs_sa/ising32/qmc2e3.txt qmc --trials 100 --P 60 --PTxJ 25 --MCSxS 2000;

# ising32 SA
../solve ../data/ising32.txt ../results/qmc_vs_sa/ising32/sa010.txt sa --trials 100 --MCSxS 10;
../solve ../data/ising32.txt ../results/qmc_vs_sa/ising32/sa100.txt sa --trials 100 --MCSxS 100;
../solve ../data/ising32.txt ../results/qmc_vs_sa/ising32/sa500.txt sa --trials 100 --MCSxS 500;
../solve ../data/ising32.txt ../results/qmc_vs_sa/ising32/sa1e3.txt sa --trials 100 --MCSxS 1000;
../solve ../data/ising32.txt ../results/qmc_vs_sa/ising32/sa2e3.txt sa --trials 100 --MCSxS 2000;