#!/bin/bash

../solve ../data/coefs0.txt ../results/QMC_sched.txt \
    qmc --trials 3 --P 60 --PTxJ 25 --MCSxS 100 --schedule ../data/schedule.txt;
