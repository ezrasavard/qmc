import math
import matplotlib.pyplot as plt
import numpy as np
import random

class pdf():

    def get_pdf(self, size, xi, xf):

        assert type(size) is int
        i_list = np.mgrid[xi:xf:eval(str(size)+'j')]
        pdf = []
        x_list = []
        for x in i_list:
            pdf.append(self.p(x))
            x_list.append(x)

        return x_list, pdf

class boltzmann(pdf):

    def __init__(self, T=1., k=1., normed=True):
        assert T != 0
        assert k != 0
        self.k = float(k)
        self.T = T
        self.normed = normed
        self.name = 'Boltzmann'

    def p(self, x):

        kT = self.k*self.T
        p = math.exp(-x/kT)
        if self.normed:
            return (1/kT)*p
        else:
            return p

class bimodal(pdf):

    def __init__(self, a=2, b=10, c=0.3):
        self.a = float(a)
        self.b = float(b)
        self.c = float(c)
        self.name = 'Bimodal'

    def p(self, x):

        a = self.a
        b = self.b
        c = self.c
        p = c*math.exp(-a*(x**2)) + (1-c)*math.exp(-a*((x-b)**2))
        return p


class metropolis_sampler():

    def __init__(self, N, pdf, trial_dists=['uniform'], ret=1000, bins=50, xi=0, xf=1, SA=False):
        # samples a given PDF with N iterations
        # plots and saves last 'ret' values

        assert type(ret) is int
        assert type(N) is int

        self.pdf = pdf
        self.pdf_name = pdf.name
        self.xi = xi
        self.xf = xf
        self.ret = ret

        self.SA = SA
        if SA:
            name = 'Simulated Annealing'
        else:
            name = 'MCMC Sampling'
        data = {name : self.mcmc(N, xi, xf, ret)}

        self.plot_data(data, bins)

    def plot_data(self, data, bins, errors_table=False):

        dist = self.pdf.get_pdf(self.ret, self.xi, self.xf)
        dist = np.array(dist)
        
        plots = {}
        for name, raw_data in data.iteritems():
            plots[name] = self.format_data(raw_data, bins)

        if errors_table:
            error_values = {}
            for name, plot in plots.iteritems():
                error_values[name] = self.calc_error(plot[1], dist[1])

            rows = []
            columns = ["Cosine Similarity", "Mean-Square Error"]
            cell_text = []
            colWidths = []
            for name in error_values:
                rows.append(name)
                cell_text.append(["%.4f" % x for x in error_values[name]])
                colWidths.append(0.4)
            the_table = plt.table(cellText=cell_text,
                                  colWidths=colWidths,
                                  rowLabels=rows,
                                  colLabels=columns,
                                  bbox=[0.172,0,.7,0.2])
            the_table.set_fontsize(16)


        plt.plot(*dist, color='r', linewidth=4,
                 label="{0} Distribution".format(self.pdf_name))

        for name, data in plots.iteritems():
            color = np.random.rand(3,1)
            plt.plot(data[0], data[1], alpha=0.75, linewidth=2,
                    label=name)

        if self.SA:
            plt.title("Simulated Annealing Test")
        else:
            plt.title("Sampling with Metropolis-Hastings")
        plt.xlim(self.xi,self.xf)
        plt.ylim(-0.4, 1.6)
        plt.grid(True)
        plt.legend()
        plt.show()

    def calc_error(self, sim, target):

        # sample target to size(sim)
        S = np.zeros((len(target), len(sim)))
        m = len(target)/len(sim) # integer division
        j = 0
        for i in range(0,len(S)):
            if i % m == 0:
                S[i][j] = 1
                j += 1
        
        t = np.dot(target, S)
        dot = np.dot(sim,t)
        err = dot/(np.linalg.norm(sim)*np.linalg.norm(t))
        mse = (abs(sim-t)**2).mean()

        return err,mse

    def format_data(self, raw, bins):

        hist = np.histogram(raw, bins=bins, density=True)
        scaled_counts = hist[0]/max(hist[0])
        data = np.array(hist[1][:-1]), np.array(scaled_counts)

        return data

    def mcmc(self, N, xi, xf, ret=None):
        # produce a Markov chain that samples a distribution

        states = []
        ret = ret or N
        U = lambda xi,xf: np.random.uniform(xi,xf)
        q = lambda u,s: np.random.normal(u, s)

        T = 1.0
        incr = 1.0/N
        current = U(xi,xf)
        p_current = self.pdf.p(current)**(1/T)
        for i in range(0,N):
            if self.SA:
                if T > 1e-6:
                    T -= incr
            states.append(current)
            next_hop = q(current,(.5*abs(xi-xf)))
            p_next = self.pdf.p(next_hop)**(1/T)
            if p_current == 0:
                p_current = 1e-16
            p = min(1, (p_next/p_current))
            if p > np.random.uniform(0,1):
                current = next_hop
                p_current = p_next

        return np.array(states[-ret:])

if __name__ == "__main__":
    bimodal = bimodal()
    boltz = boltzmann()
    sampler3 = metropolis_sampler(1000000, pdf=bimodal, ret=10000, bins=50, xi=-3, xf=15)
    sampler2 = metropolis_sampler(1000000, pdf=bimodal, ret=10000, bins=50, xi=-3, xf=15, SA=True)
