#!/bin/bash

# Automagic XOR timesweeps
# These shouldn't be that good
./dist_match.py --qmcfile ../results/automagic_xor_times/xor040.txt --dwave ../data/xor040/sol0.json;
./dist_match.py --qmcfile ../results/automagic_xor_times/xor100.txt --dwave ../data/xor100/sol0.json;
./dist_match.py --qmcfile ../results/automagic_xor_times/xor1e3.txt --dwave ../data/xor1e3/sol0.json;
./dist_match.py --qmcfile ../results/automagic_xor_times/xor2e3.txt --dwave ../data/xor2e3/sol0.json;

# Automagic problem tests
# These should be pretty good
./dist_match.py --qmcfile ../results/automagic/xor100.txt --dwave ../data/xor100/sol0.json;
./dist_match.py --qmcfile ../results/automagic/mem100.txt --dwave ../data/mem100/sol0.json;
./dist_match.py --qmcfile ../results/automagic/maj531.txt --dwave ../data/maj531/sol0.json;
./dist_match.py --qmcfile ../results/automagic/s3inv20.txt --dwave ../data/s3inv20/sol0.json;
./dist_match.py --qmcfile ../results/automagic/wire50_20.txt --dwave ../data/wire50_20/sol0.json;
./dist_match.py --qmcfile ../results/automagic/split2.txt --dwave ../data/split2/sol0.json;
./dist_match.py --qmcfile ../results/automagic/split3.txt --dwave ../data/split3/sol0.json;
