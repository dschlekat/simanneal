#===========================================
"""
This document will contain the code for a basic application of simulated annealing, finding the global maximum of a function.

Applications: spectra max finder? (finds the peak of a spectrum, maybe even matches to known spectra along with a doppler shift estimate??)

To do:
    Finalize algorithm
    (?) Create animation capabilities to show iterations over time, turn into gif for presentation
    (?) Create an init function to display different functions to use, different iteration counts, etc. 
"""
#===========================================

#===========================================
import argparse                  
from argparse import RawTextHelpFormatter
import numpy as np
import matplotlib.pyplot as plt

import helper_functions as helper
#===========================================

#===========================================
# Probability functions to be maximized
def wave(x):
    if x >= 0 and x <= 2 * np.pi:
        y = np.sin(x) + np.sin(2*x) + np.sin(3*x)
    else:
        y = 0
    return y

def parabola1d(x):
    y = -1*(x**2) + 2
    return y

#===========================================
# Plotting function
# input : x, y : x and y values of function to plot
#         s    : global maximum
#         pFNC : function to plot
# output: plot of function
def plot_function(x, y, s, pFNC, a_type):
    if pFNC == parabola1d:
        if a_type == 'anneal':
            plt.title("Parabola Function - Annealing")
        elif a_type == 'hill':
            plt.title("Parabola Function - Hill Climbing")
        plt.plot(x, y, 'b', label="Probability Function")
        plt.vlines(s, ymin=0, ymax=pFNC(s), color='red', label="Global Maximum")
        plt.xlabel("x")
        plt.ylabel("f(x)")
        plt.legend(loc="upper right")
        plt.show()
    elif pFNC == wave:
        if a_type == 'anneal':
            plt.title("Wave Function - Annealing")
        elif a_type == 'hill':
            plt.title("Wave Function - Hill Climbing")
        plt.plot(x, y, 'b', label="Probability Function")
        plt.vlines(s, ymin=0, ymax=pFNC(s), color='red', label="Global Maximum")
        plt.xlabel("x")
        plt.ylabel("f(x)")
        plt.legend(loc="upper right")
        plt.show()

    return

#===========================================
# Simulated Annealing function
# input : s0    : initial state
#         delta : stepsize to determine new trial state x'
#         pFNC  : function to maximize
#         kmax  : max number of iterations
# output: s     : global maximum
def anneal(s0, delta, pFNC, kmax):
    s = s0
    s_best = s0
    for k in range(kmax):
        temp = 1 - (k)/kmax

        u = np.random.rand(1)

        snew = s + delta * (2*u - 1 )

        if pFNC(snew) > pFNC(s):
            s = snew
        elif np.random.rand(1) < np.exp(-(pFNC(s) - pFNC(snew))/temp): 
            s = snew
        else:
            s = s

        if pFNC(s) > pFNC(s_best):
            s_best = s

    return s_best, kmax

#===========================================
# Hill Climbing function
# input : s0    : initial state
#         delta : stepsize to determine new trial state x'
#         pFNC  : function to maximize
#         kmax  : max number of iterations
# output: s     : maximum
def hill_climb(s0, delta, pFNC, kmax):
    s = s0
    for k in range(kmax):
        snew = s + delta * (2*np.random.rand(1) - 1 )

        if pFNC(snew) > pFNC(s):
            s = snew
        else:
            s = s

    return s, kmax

#===========================================
# Initialize function
# input : p_type : string describing problem
# output: x, y   : x and y values of function to plot
#         s0     : initial state
#         pFNC   : function to maximize
def init(p_type):
    if p_type == 'parabola1d':
        x = np.linspace(-1, 1, 1000)
        y = -1*(x**2) + 2
        s0 = np.random.uniform(-1, 1)
        pFNC = parabola1d
    elif p_type == 'wave':
        x = np.linspace(0, 2*np.pi, 1000)
        y = np.sin(x) + np.sin(2*x) + np.sin(3*x)
        s0 = np.random.uniform(0, 2*np.pi)
        pFNC = wave
    else:
       print('[init]: invalid problem %s' % (p_type))
       exit()
    return x, y, s0, pFNC

#===========================================
def main():
    parser = argparse.ArgumentParser(formatter_class=RawTextHelpFormatter)
    parser.add_argument("p_type",type=str,
                        help="problem name:\n"
                             "   parabola1d   : parabola function\n"
                             "   wave         : wave function with multiple global maxima\n"
                             )
    parser.add_argument("a_type",type=str,
                        help="algorithm name:\n"
                            "   anneal   : simulated annealing\n"
                            "   hill     : hill climbing\n"
                             )
    parser.add_argument("K",type=int,
                        help="max number of iterations")
    parser.add_argument("delta",type=float,
                        help="stepsize to determine new trial state x'")


    args                     = parser.parse_args()
    p_type                   = args.p_type
    a_type                   = args.a_type
    K                        = args.K
    delta                    = args.delta
    x, y, s0, pFNC = init(p_type)
    

    if a_type == 'anneal':
        s, iters = anneal(s0, delta, pFNC, K)
    elif a_type == 'hill':
        s, iters = hill_climb(s0, delta, pFNC, K)


    if pFNC == charbonneau2:
        s = s.tolist()
        s[0] = float(s[0])
        s[1] = float(s[1])
        print("Found maximum at x= %1.3f, y= %1.3f" % (s[0], s[1]))
    else:
        s = float(s)
        print("Found maximum at x= %1.3f" % s)

    print("Iterations: ", iters)
    plot_function(x, y, s, pFNC, a_type)
#===========================================

main()