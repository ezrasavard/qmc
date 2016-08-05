#!/usr/bin/python

import numpy as np
import matplotlib.pyplot as plt 
import sys

if __name__ == "__main__":
    data = np.load(sys.argv[1])
    x = data[:,0]
    y = data[:,1]
    z = data[:,2]

    block_size = (np.max(x) - np.min(x))**2
#     plt.scatter(x,y,c=z,s=block_size,alpha=0.5,edgecolors='face',marker='s')
#     plt.scatter(x,y,c=z,s=block_size,edgecolors='face',marker='s', cmap=plt.cm.Reds)
    plt.scatter(x,y,c=z,s=block_size,edgecolors='face',marker='s')
    plt.xlim(np.min(x),np.max(x))
    plt.ylim(np.min(y),np.max(y))
    plt.xlabel("PTxJ")
    plt.ylabel("MCSxS")
    cb = plt.colorbar()
    cb.set_label('Differences')
    plt.title(sys.argv[2])
    plt.show()
