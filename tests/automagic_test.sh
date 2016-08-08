#!/bin/bash

../solve ../data/xor100/sol0.txt ../results/automagic/xor100.txt qmc --trials 100 --automagic --schedule ../data/schedule.txt
../solve ../data/mem100/sol0.txt ../results/automagic/mem100.txt qmc --trials 100 --automagic --schedule ../data/schedule.txt
../solve ../data/s3inv20/sol0.txt ../results/automagic/s3inv20.txt qmc --trials 100 --automagic --schedule ../data/schedule.txt
../solve ../data/maj531/sol0.txt ../results/automagic/maj531.txt qmc --trials 100 --automagic --schedule ../data/schedule.txt
../solve ../data/split2/sol0.txt ../results/automagic/split2.txt qmc --trials 100 --automagic --schedule ../data/schedule.txt
../solve ../data/split3/sol0.txt ../results/automagic/split3.txt qmc --trials 100 --automagic --schedule ../data/schedule.txt
../solve ../data/wire50_20/sol0.txt ../results/automagic/wire50_20.txt qmc --trials 100 --automagic --schedule ../data/schedule.txt

