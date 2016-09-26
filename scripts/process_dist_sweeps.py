#!/usr/bin/python

import copy
import fnmatch
import matplotlib.pyplot as plt
import numpy as np
import os
import string
import sys

import lib_dist_sweeps as lib


if __name__ == "__main__":

    results = []
    plots = []
    # 1. walk through directories and locate test results
    # 2. locate corresponding dwave output
    # directories are laid out to have "circuitname/runtime/files" in the path
    # traverse root directory, and list directories as dirs and files as files
    for root, dirs, files in os.walk(sys.argv[1]):
        path = os.path.relpath(root).split(os.sep)
        if path[-1][0] == 'N':
            continue
        if path[-1] != sys.argv[2]:
            continue
        if files != []:
            outfile = os.path.join(root, string.join(["data", path[-2], path[-1], ".npy"],"_"))
            fnames = [os.path.join(root,name) for name in files if fnmatch.fnmatch(name, "*.txt")]
            if fnames == []:
                continue
            dwave_file = copy.copy(path)
            dwave_file[1] = "data"
            dwave_file.append("sol0.json")
            dwave_file = os.path.join(*dwave_file)
            results.append((fnames,path,outfile,dwave_file))

    # 3. process each set of results (difference calcs)
    # 4. gather problem data into useful variables (N, problem_name)
    # 5. optionally produce individual dist-match style plots
    for files, path, outfile, dwave_file in results:
        data = lib.calc_diffs(files, dwave_file, make_plots=True, outfile=outfile, ret=True)

        # 6. optionally produce heatmaps for each set
        if "--heatmap" in sys.argv:
            plotfile = os.path.join(os.path.join(*path), "heatmap.png")
            runtime = path[-1] + "us"
            title = string.join(["differences for ", path[-2], runtime]," ")
            print("making heatmap: {}\n".format(plotfile))
            lib.make_heatmap(data, title, plotfile)

        # 7. reduce dataset to the best 5%
        data = lib.best_diffs(data, ret=True, plot=False)

# 8. extract pairs of (PTxJ, MCSxS) for the lowest MCSxS value at each PTxJ
#         uniques = np.unique(data[:,0])
#         reduced_data = [[ptxj, np.min(data[data[:,0] == ptxj][:,1])] for ptxj in uniques]
#         reduced_data = np.array(reduced_data)
        reduced_data = data

        if "--nofit" in sys.argv:
            continue

# 9. curve fit each one with a prototype function (scipy.optimize)
# 10. calculate a transform to fit the curves with x and y as functions of N
        datafile = os.path.join(os.path.join(*path), "curvefit.npy")
        print("curve fitting: {}\n".format(datafile))
        input_file = copy.copy(path)
        input_file[1] = "data"
        input_file.append("sol0.txt")
        input_file = os.path.join(*input_file)
        N = lib.get_N(input_file)

        # maps MCSxS to a function of N and PTxJ
        tx = lib.Transformer(reduced_data, N)
        plots.append((path, tx))

# 10.b. map PTxJ as function of N using medians in tx.xmed
    if "--nofit" in sys.argv:
        sys.exit()
    ptxj_data = np.array([[tx.xmed, tx.N] for path, tx in plots])
    ptxj_args = lib.fit_PTxJ(ptxj_data[:,0], ptxj_data[:,1])


# 11b. produce a plot of untransformed data
    plt.figure()
    plt.xlabel("PTxJ")
    plt.ylabel("MCSxS")
    plt.title("Location of Best Matches")
    for path, tx in plots:
        label = "{}, {}us".format(path[-2], path[-1])
        data = tx.data[tx.data[:,0].argsort()]
        plt.plot(data[:,0], data[:,1], '-o',label=label)
    plotfile = os.path.join(sys.argv[1], "bestmatch_curves.png")
    plt.legend(loc='best')
    print("plotting curve fits: {}\n".format(plotfile))
    plt.savefig(plotfile, bbox_inches='tight', format='png')
    plt.close()

# 11. produce a plot of the set of curves, transformed into a grouping
    plt.figure()
    plt.xlabel("PTxJ")
    plt.ylabel("MCSxS")
    plt.title("Set of Curves Predicting Best Results")
    xdata = [x for x in range(0,100)]
    mcsxs_args = []
    allx = []
    ally = []
    for path, tx in plots:
        ydata = [tx.MCSxSfunc(x, *tx.mcsxs_args) for x in xdata]
        label = "{}, {}us".format(path[-2], path[-1])
        plt.plot(xdata, ydata, '-o', label=label)
        mcsxs_args.append(tx.mcsxs_args)
        allx += list(tx.x)
        ally += list(tx.y)
    plotfile = os.path.join(sys.argv[1], "prediction_curves.png")
    datalist = [[x, y] for x, y in zip(allx, ally)]
    all_data = np.array(datalist)
    args = lib.fit_PTxJ(all_data[:,1], all_data[:,0]) # equation has same form
    xdata = range(1,100)
    ydata = lib.PTxJfunc(xdata, *args)
    label = "Best Fit"
    plt.plot(xdata, ydata, 'rx', label=label, alpha=.6, linewidth=6)
    plt.legend(loc='best')
    print("plotting curve fits: {}\n".format(plotfile))
    plt.savefig(plotfile, bbox_inches='tight', format='png')
    plt.close()

# 12. Calculate some mean arguments off mcsxs_args, save them as a string
#     mcsxs_string = lib.MCSxSmap(mcsxs_args)
    mcsxs_string = lib.MCSxSmap2(args)
    ptxj_string = lib.PTxJmap(ptxj_args)

    outfile = os.path.join(sys.argv[1], "prediction_equations.dat")
    print("writing curve equations: {}\n".format(outfile))
    with open(outfile, 'w') as fp:
        fp.write(ptxj_string)
        fp.write("\n")
        fp.write(mcsxs_string)
        fp.write("\n")
