#!/usr/bin/python

import sys

import lib_dist_sweeps as lib


if __name__ == "__main__":

    results = []
    # 1. walk through directories and locate test results
    # 2. locate corresponding dwave output
    # directories are laid out to have "circuitname/runtime/files" in the path
    # traverse root directory, and list directories as dirs and files as files
    for root, dirs, files in os.walk(sys.argv[1]):
        if files != []:
            path = os.path.relpath(root).split(os.sep)
            outfile = os.path.join(root, string.join(["data", path[-2], path[-1], ".npy"],"_"))
            results.append((path,outfile))

    # 3. process each set of results (difference calcs)
    # 4. gather problem data into useful variables (N, problem_name)
    # 5. optionally produce individual dist-match style plots
    for path, outfile in results:
        data = lib.calc_diffs(infile_dir, make_plots=True, kT=50, outfile=outfile, ret=True)

        # 6. optionally produce heatmaps for each set
        if "--heatmap" in sys.argv:
            plotfile = os.path.join(path, "heatmap.png")_
            lib.make_heatmap(data, title, plotfile)

        # 7. reduce dataset to the best 5%
        data = lib.best_diffs(data, ret=True, plot=False):
        # throwaway noise at edges
        data = data[data[:,0] > 8]
        data = data[data[:,1] > 14]


# 8. extract pairs of (PTxJ, MCSxS) for the lowest MCSxS value at each PTxJ

# 9. curve fit each one with a prototype function (scipy.optimize)
# 10. optionally produce plots with this data and their curve fits
# 11. calculate a transform to fit the curves with x and y as functions of N
# 12. produce a plot of the set of curves, transformed into a grouping
