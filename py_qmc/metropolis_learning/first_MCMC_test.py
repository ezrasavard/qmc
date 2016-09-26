import math
import matplotlib.pyplot as plt
import numpy as np
import random

def boltzmann_probz(x, T=1., k=1.):
    # return boltzmann probability of x

    assert T != 0
    assert k != 0
    k = float(k)
#     return (1./(k*T))*math.exp(-x/(k*T))
    return math.exp(-x/(k*T))

def boltzmann_mcmc(N, ret=None, T=300.,k=1.):
    # produce a Markov chain that samples a boltzmann distribution
    states = []
    ret = ret or N
    current = random.uniform(0,1)
    for i in range(0,N):
        states.append(current)
        next_hop = random.uniform(0,1)
        p_current = boltzmann_probz(current)
        p_next = boltzmann_probz(next_hop)
        p = min(1, (p_next/p_current))
        if p > random.uniform(0,1):
            current = next_hop

    return states[-ret:]

if __name__ == "__main__":
    N = 100000
    i_list = np.mgrid[0:1:1000j]
    size = len(i_list)
    mcmc = boltzmann_mcmc(N, size)
    boltz = []
    x_list = []
    for x in i_list:
        boltz.append(boltzmann_probz(x))
        x_list.append(x)

    plt.plot(x_list, boltz, 'r', linewidth=2, label="Boltzmann Distribution")
    bins =25 
    hist1 = np.histogram(mcmc, bins=bins, density=True)
    height = max(hist1[0])
    print height
    plt.bar(hist1[1][:-1], hist1[0]/height, width=0.04, alpha=0.55,color='g',
            label="MCMC Simulation Results")

    plt.title("Sampling Boltzmann Distribution with Metropolis-Hastings")
    plt.axis([0, 1, 0, 1.2])
    plt.grid(True)
    plt.legend()
    plt.show()
