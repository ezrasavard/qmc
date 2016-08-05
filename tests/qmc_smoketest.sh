#!/bin/bash

../solve ../data/coefs0.txt ../results/QMC_smoke.txt \
    qmc --trials 3 --P 60 --PTxJ 25 --MCSxS 100;
sleep 1;
cat ../results/QMC_smoke.txt
echo ""

