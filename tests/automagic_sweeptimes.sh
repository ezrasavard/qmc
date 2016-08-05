#!/bin/bash

../solve ../data/xor040/sol0.txt ../results/automagic_xor_times/xor040.txt qmc --trials 100 --automagic
../solve ../data/xor1e3/sol0.txt ../results/automagic_xor_times/xor1e3.txt qmc --trials 100 --automagic
../solve ../data/xor2e3/sol0.txt ../results/automagic_xor_times/xor2e3.txt qmc --trials 100 --automagic
