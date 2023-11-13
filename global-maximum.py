"""
This document will contain the code for a basic application of simulated annealing, finding the global maximum of a function.

Applications: spectra max finder? (finds the peak of a spectrum, maybe even matches to known spectra along with a doppler shift estimate??)

To do:
    Finalize algorithm
    (?) Create animation capabilities to show iterations over time, turn into gif for presentation
    (?) Create an init function to display different functions to use, different iteration counts, etc. 
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
    y = np.sin(x) + np.sin(2*x) + np.sin(3*x)
    return y

def p(x):

    if x >= 0 and x <= 2 * np.pi:
        y = np.sin(x) + np.sin(2*x) + np.sin(3*x)
    else:
        y = 0
    return y

def plot_function(x, y, s):
    """
    Plot the function we want to maximize.
    """
    plt.plot(x, y, 'b', label="Test Function")
    plt.plot(s, f(s), 'r.', markersize=10, label="Global Maximum")
    plt.xlabel("x")
    plt.ylabel("f(x)")
    plt.legend(loc="upper right")
    plt.show()
    return

def anneal(s0, delta, kmax):
    s = s0
    for k in range(kmax):
        temp = 1 - (k+1)/kmax

        neighbors = [s + delta, s - delta]
        rn.shuffle(neighbors)

        u = np.random.rand(1)

        neighbor = s + delta * (2* u - 1 )
        snew = neighbor

        if p(snew) > p(s):
            s = snew
        else: 
            f = np.exp(-(p(s) - p(snew))/temp)
            if rn.random() < f:
                s = snew

    return s, kmax

def main():
    """
    Main function.
    """
    x = np.linspace(0, 2*np.pi, 1000)
    y = f(x)

    s0 = rn.uniform(0, 2*np.pi)
    print("Starting point: ",s0)

    delta = 1.
    iters = 100000

    s, iters = anneal(s0, delta, iters)

    s = float(s)
    print("Found maximum at x= %1.3f" % s)
    print("Iterations: ", iters)

    plot_function(x, y, s)

main()