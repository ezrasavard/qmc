# 1. walk through directories and locate test results
# 2. locate corresponding dwave output
# 3. process each set of results (difference calcs)
# 4. gather problem data into useful variables (N, problem_name)
# 5. optionally produce individual dist-match style plots
# 6. optionally produce heatmaps for each set
# 7. reduce dataset to the best 5%
# 8. extract pairs of (PTxJ, MCSxS) for the lowest MCSxS value at each PTxJ
# 9. curve fit each one with a prototype function (scipy.optimize)
# 10. optionally produce plots with this data and their curve fits
# 11. calculate a transform to fit the curves with x and y as functions of N
# 12. produce a plot of the set of curves, transformed into a grouping
