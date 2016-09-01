#!/usr/bin/python

import lib_dwave as dwave
import lib_dist_sweeps as lib

if __name__ == "__main__":

    qmc_names = []
    outfile = "diffs.npy"
    if sys.argv[1] == "--qmc":
        fdir = sys.argv[2]
        for fname in os.listdir(fdir):
            if fnmatch.fnmatch(fname, '*.txt'):
                qmc_names.append(os.path.join(fdir,fname))

        qmc_names.sort(key=str.lower)
    elif sys.argv[1] == "--qmcfile":
        fdir, fname = os.path.split(sys.argv[2])
        qmc_names.append(sys.argv[2])
        outfile = string.split(fname,'.')[0] + "_diffs.npy"
        print outfile

    if sys.argv[3] == "--dwave":
        dwave_file = sys.argv[4]
        counts, e = dwave.load_jakes_dwave_data(dwave_file)
        state_array = []
        for i, count in enumerate(counts):
            state_array += [e[i] for x in range(0,count)]

    if "--sweep" in sys.argv:
        for kT in np.linspace(.5,50,10):
            outfile = "diffs_{}.npy".format(kT)
            lib.calc_diffs(qmc_names, make_plots=False, kT=kT, outfile=outfile)
    else:
        lib.calc_diffs(qmc_names, make_plots=True, kT=50, outfile=outfile)
