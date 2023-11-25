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
def charbonneau2(x,**kwargs):
    r1s = (x[0]-0.5)**2 + (x[1]-0.5)**2
    r2s = (x[0]-0.6)**2 + (x[1]-0.1)**2
    s1s = 0.09
    s2s = 0.0009
    a   = 0.8
    b   = 0.879008
    return a*np.exp(-r1s/s1s)+b*np.exp(-r2s/s2s)

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
def plot_function(x, y, s, pFNC):
    if pFNC == parabola1d:
        plt.title("Parabola Function")
        plt.plot(x, y, 'b', label="Probability Function")
        plt.plot(s, pFNC(s), 'r.', markersize=10, label="Global Maximum")
        plt.xlabel("x")
        plt.ylabel("f(x)")
        plt.legend(loc="upper right")
        plt.show()
    elif pFNC == wave:
        plt.title("Wave Function")
        plt.plot(x, y, 'b', label="Probability Function")
        plt.plot(s, pFNC(s), 'r.', markersize=10, label="Global Maximum")
        plt.xlabel("x")
        plt.ylabel("f(x)")
        plt.legend(loc="upper right")
        plt.show()
    elif pFNC == charbonneau2:
        plt.title("Charbonneau 2D Function")
        plt.plot(x, y, 'b', label="Probability Function")
        plt.plot(s[0], s[1], 'r.', markersize=10, label="Global Maximum")
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
    elif p_type == 'charbonneau2':
        x = np.linspace(0, 1, 1000)
        y = charbonneau2(x)
        s0 = np.random.uniform(0, 1, 2)
        pFNC = charbonneau2
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
                             "   charbonneau2 : 2D Charbonneau function\n"
                             )
    parser.add_argument("K",type=int,
                        help="max number of iterations")
    parser.add_argument("delta",type=float,
                        help="stepsize to determine new trial state x'")


    args                     = parser.parse_args()
    p_type                   = args.p_type
    K                        = args.K
    delta                    = args.delta
    x, y, s0, pFNC = init(p_type)

    

    s, iters = anneal(s0, delta, pFNC, K)

    if pFNC == charbonneau2:
        s = s.tolist()
        s[0] = float(s[0])
        s[1] = float(s[1])
        print("Found maximum at x= %1.3f, y= %1.3f" % (s[0], s[1]))
    else:
        s = float(s)
        print("Found maximum at x= %1.3f" % s)
    print("Iterations: ", iters)

    plot_function(x, y, s, pFNC)
#===========================================

main()