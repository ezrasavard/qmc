#!/usr/bin/python

# Thanks to StackOverflow user Joe Kington for the great examples
# http://stackoverflow.com/questions/9401658/matplotlib-animating-a-scatter-plot

import math
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import sys

class AnimatedScatter(object):
    """An animated scatter plot using matplotlib.animations.FuncAnimation."""

    def __init__(self, datafile):
        self.data = self.process(datafile)
        self.stream = self.data_stream()
        self.landscape = [] # list of explored points

        # Setup the figure and axes...
        self.fig, self.ax = plt.subplots()

        # Then setup FuncAnimation.
        self.ani = animation.FuncAnimation(self.fig, self.update, interval=100, 
                                           init_func=self.setup_plot, blit=True)

    def setup_plot(self):
        """Initial drawing of the scatter plot."""
        self.bg = self.ax.scatter([], [], c='g', edgecolor='g', s=64, alpha=0.3, animated=True)
        self.scats = []
        self.scats.append(self.bg)

        self.gamma = self.ax.text(0.1, 0.9, '', horizontalalignment='left',
                fontsize=20, transform=self.ax.transAxes)
        self.scats.append(self.gamma)

        for k in self.slices:
            self.scats.append(self.ax.scatter([], [], c='r', s=200, alpha=0.5, animated=True))

        self.ax.set_title(self.title)
        self.ax.set_xlabel("Reduced Configuration Space")
        self.ax.set_ylabel("Configuration Energy")
        x_list = [math.ceil(np.float64(row[1])) for row in self.data]
        y_list = [math.ceil(np.float64(row[2])) for row in self.data]
        self.ax.axis([0, max(x_list), min(y_list) - .2*(abs(min(y_list))), max(y_list) + .2*(abs(max(y_list)))])
        self.ax.grid(True)

        # For FuncAnimation's sake, we need to return the artist we'll be using
        return self.scats


    def process(self, datafile):
        """Format data list from file"""

        # read data from the file
        with open(sys.argv[1]) as fp:
            data = fp.readlines()

        # top three lines are header stuff
        self.title = data.pop(0)
        self.params = data.pop(0)
        self.problem_info = data.pop(0)

        # three columns for SA
        # shedule value, energy of config, config as hex
        data = [x.split(",") for x in data]
        ret = []
        states = {}
        i = 0
        for sched, y, x, k in data:
            if x not in states:
                states[x] = i
                i += 1
            ret.append((sched, states[x], y, int(k)))

        self.slices = set(int(row[3]) for row in data)
        self.slices.remove(-1)

        return ret


    def data_stream(self):
        """Stream rows of data list"""

        # data as (sched, x, y)
        for row in self.data:
            yield row


    def update(self, i):
        """Update the scatter plot."""

        # data as (sched, x, y)
        sched, x, y, k = next(self.stream)

        # update the landscape
        self.landscape.append((x, y))
        self.bg.set_offsets(self.landscape)

        # update the title
        self.gamma.set_text("G = {:.4f}".format(float(sched)))

        # Set x and y data...
        if k == -1:
            # update all slices
            for p in self.scats[2:]:
                p.set_offsets((x, y))
        else:
            self.scats[k+2].set_offsets((x, y))

        # We need to return the updated artist for FuncAnimation to draw..
        return self.scats


    def show(self):
        plt.show()

if __name__ == '__main__':

    a = AnimatedScatter(sys.argv[1])
    a.ani.save('animation_qmc-{}.mp4'.format(sys.argv[1].split('.')[0]), fps=30, extra_args=['-vcodec', 'libx264'])
    a.show()
