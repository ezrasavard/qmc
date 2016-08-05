#!/bin/bash

# MEM QMC PTxJ Sweep
#10
../solve ../data/mem100/sol0.txt ../results/qmc_PTxJ_sweep/mem/qmc_010_020.txt qmc --trials 100 --P 60 --PTxJ 2 --MCSxS 10;
../solve ../data/mem100/sol0.txt ../results/qmc_PTxJ_sweep/mem/qmc_010_100.txt qmc --trials 100 --P 60 --PTxJ 10 --MCSxS 10;
../solve ../data/mem100/sol0.txt ../results/qmc_PTxJ_sweep/mem/qmc_010_250.txt qmc --trials 100 --P 60 --PTxJ 25 --MCSxS 10;
../solve ../data/mem100/sol0.txt ../results/qmc_PTxJ_sweep/mem/qmc_010_500.txt qmc --trials 100 --P 60 --PTxJ 50 --MCSxS 10;
../solve ../data/mem100/sol0.txt ../results/qmc_PTxJ_sweep/mem/qmc_010_750.txt qmc --trials 100 --P 60 --PTxJ 75 --MCSxS 10;
../solve ../data/mem100/sol0.txt ../results/qmc_PTxJ_sweep/mem/qmc_010_990.txt qmc --trials 100 --P 60 --PTxJ 99 --MCSxS 10;
#100
../solve ../data/mem100/sol0.txt ../results/qmc_PTxJ_sweep/mem/qmc_100_020.txt qmc --trials 100 --P 60 --PTxJ 2 --MCSxS 100;
../solve ../data/mem100/sol0.txt ../results/qmc_PTxJ_sweep/mem/qmc_100_100.txt qmc --trials 100 --P 60 --PTxJ 10 --MCSxS 100;
../solve ../data/mem100/sol0.txt ../results/qmc_PTxJ_sweep/mem/qmc_100_250.txt qmc --trials 100 --P 60 --PTxJ 25 --MCSxS 100;
../solve ../data/mem100/sol0.txt ../results/qmc_PTxJ_sweep/mem/qmc_100_500.txt qmc --trials 100 --P 60 --PTxJ 50 --MCSxS 100;
../solve ../data/mem100/sol0.txt ../results/qmc_PTxJ_sweep/mem/qmc_100_750.txt qmc --trials 100 --P 60 --PTxJ 75 --MCSxS 100;
../solve ../data/mem100/sol0.txt ../results/qmc_PTxJ_sweep/mem/qmc_100_990.txt qmc --trials 100 --P 60 --PTxJ 99 --MCSxS 100;
#500
../solve ../data/mem100/sol0.txt ../results/qmc_PTxJ_sweep/mem/qmc_500_020.txt qmc --trials 100 --P 60 --PTxJ 2 --MCSxS 500;
../solve ../data/mem100/sol0.txt ../results/qmc_PTxJ_sweep/mem/qmc_500_100.txt qmc --trials 100 --P 60 --PTxJ 10 --MCSxS 500;
../solve ../data/mem100/sol0.txt ../results/qmc_PTxJ_sweep/mem/qmc_500_250.txt qmc --trials 100 --P 60 --PTxJ 25 --MCSxS 500;
../solve ../data/mem100/sol0.txt ../results/qmc_PTxJ_sweep/mem/qmc_500_500.txt qmc --trials 100 --P 60 --PTxJ 50 --MCSxS 500;
../solve ../data/mem100/sol0.txt ../results/qmc_PTxJ_sweep/mem/qmc_500_750.txt qmc --trials 100 --P 60 --PTxJ 75 --MCSxS 500;
../solve ../data/mem100/sol0.txt ../results/qmc_PTxJ_sweep/mem/qmc_500_990.txt qmc --trials 100 --P 60 --PTxJ 99 --MCSxS 500;
#1000
../solve ../data/mem100/sol0.txt ../results/qmc_PTxJ_sweep/mem/qmc_1e3_020.txt qmc --trials 100 --P 60 --PTxJ 2 --MCSxS 1000;
../solve ../data/mem100/sol0.txt ../results/qmc_PTxJ_sweep/mem/qmc_1e3_100.txt qmc --trials 100 --P 60 --PTxJ 10 --MCSxS 1000;
../solve ../data/mem100/sol0.txt ../results/qmc_PTxJ_sweep/mem/qmc_1e3_250.txt qmc --trials 100 --P 60 --PTxJ 25 --MCSxS 1000;
../solve ../data/mem100/sol0.txt ../results/qmc_PTxJ_sweep/mem/qmc_1e3_500.txt qmc --trials 100 --P 60 --PTxJ 50 --MCSxS 1000;
../solve ../data/mem100/sol0.txt ../results/qmc_PTxJ_sweep/mem/qmc_1e3_750.txt qmc --trials 100 --P 60 --PTxJ 75 --MCSxS 1000;
../solve ../data/mem100/sol0.txt ../results/qmc_PTxJ_sweep/mem/qmc_1e3_990.txt qmc --trials 100 --P 60 --PTxJ 99 --MCSxS 1000;
#2000
../solve ../data/mem100/sol0.txt ../results/qmc_PTxJ_sweep/mem/qmc_2e3_020.txt qmc --trials 100 --P 60 --PTxJ 2 --MCSxS 2000;
../solve ../data/mem100/sol0.txt ../results/qmc_PTxJ_sweep/mem/qmc_2e3_100.txt qmc --trials 100 --P 60 --PTxJ 10 --MCSxS 2000;
../solve ../data/mem100/sol0.txt ../results/qmc_PTxJ_sweep/mem/qmc_2e3_250.txt qmc --trials 100 --P 60 --PTxJ 25 --MCSxS 2000;
../solve ../data/mem100/sol0.txt ../results/qmc_PTxJ_sweep/mem/qmc_2e3_500.txt qmc --trials 100 --P 60 --PTxJ 50 --MCSxS 2000;
../solve ../data/mem100/sol0.txt ../results/qmc_PTxJ_sweep/mem/qmc_2e3_750.txt qmc --trials 100 --P 60 --PTxJ 75 --MCSxS 2000;
../solve ../data/mem100/sol0.txt ../results/qmc_PTxJ_sweep/mem/qmc_2e3_990.txt qmc --trials 100 --P 60 --PTxJ 99 --MCSxS 2000;

#SA
../solve ../data/mem100/sol0.txt ../results/qmc_vs_sa/mem/sa010.txt sa --trials 100 --MCSxS 10;
../solve ../data/mem100/sol0.txt ../results/qmc_vs_sa/mem/sa100.txt sa --trials 100 --MCSxS 100;
../solve ../data/mem100/sol0.txt ../results/qmc_vs_sa/mem/sa500.txt sa --trials 100 --MCSxS 500;
../solve ../data/mem100/sol0.txt ../results/qmc_vs_sa/mem/sa1e3.txt sa --trials 100 --MCSxS 1000;
../solve ../data/mem100/sol0.txt ../results/qmc_vs_sa/mem/sa2e3.txt sa --trials 100 --MCSxS 2000;