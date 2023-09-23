"""
This document will contain the code for a basic application of simulated annealing, finding the global maximum of a function.
"""

# IMPORTS
import numpy as np
import matplotlib.pyplot as plt
import random as rn

## you probably won't need these, but they can help make things look nicer
from IPython.display import Latex
from matplotlib.colors import LogNorm
from matplotlib import colors

def f(x):
    """
    Plots a simple function to be maximized. Contains multiple local maxima.
    """
    return np.sin(x) + np.sin(2*x) + np.sin(3*x)

def plot_function(x, y, s):
    """
    Plot the function we want to maximize.
    """
    plt.plot(x, y, 'b', label="Test Function")
    plt.plot(s, f(s), 'r.', markersize=10, label="Global Maximum")
    plt.xlabel("x")
    plt.ylabel("f(x)")
    plt.show()

def anneal(s0, kmax):
    s = s0
    for k in range(kmax):
        temp = 1 - (k+1)/kmax
        neighbors = [s + 0.1, s - 0.1]
        rn.shuffle(neighbors)
        snew = neighbors[0]

        if f(snew) > f(s):
            s = snew

    return s, kmax

def main():
    """
    Main function.
    """
    x = np.linspace(0, 2*np.pi, 1000)
    y = f(x)

    s0 = x[0]
    print("Starting point: ",s0)

    iters = 1000

    s, iters = anneal(s0, iters)

    s = float(s)
    print("Found maximum at x= %1.3f" % s)
    print("Iterations: ", iters)

    plot_function(x, y, s)

main()