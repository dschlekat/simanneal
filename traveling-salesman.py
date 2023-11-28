"""
This document will contain the code for the classic traveling salesman problem, solved using simulated annealing.
"""
#===========================================
import argparse                  
from argparse import RawTextHelpFormatter
import numpy as np
import matplotlib.pyplot as plt

import helper_functions as helper
#===========================================

#===========================================
# Returns model parameters depending on problem name
# input : p_type : string describing problem
#         N      : number of stops
# output: coords : positions of stops, list of 2 or 3D arrays
def init(p_type, N):
    if (p_type == 'random2D'):
        coords = helper.rand_cities(int(N),2)
    elif (p_type == 'random3D'):
        coords = helper.rand_cities(int(N),3)
    elif (p_type == 'USA'):
        coords = helper.USA_cities(int(N))
    else:
        raise Exception("[init]: invalid p_type = %s" % (p_type))

    return coords

#===========================================
# Returns energy of a path
# input : S      : order of path
#         coords : positions of stops, list of 2 or 3D arrays
# output: E      : energy of path
def energy(S, coords):
    E = 0
    N = len(coords)

    for i in range(N):
        E = E + np.linalg.norm(coords[S[i]] - coords[S[(i+1)%N]])

    return E

#===========================================
# Simulated annealing algorithm
# input : coords : positions of stops, list of 2 or 3D arrays
#         delta  : stepsize to determine new trial state x'
#         K      : max number of iterations
# output: X      : list of best paths
#         E      : list of energies
def anneal_path(coords, K):
    N = len(coords)
    S0 = np.random.permutation(N)
    S = S0

    for k in range(K):
        temp = 1 - k/K

        u = np.random.uniform(-1,1)
        if u < 0:
            # randomly swap two cities
            i = np.random.randint(0,N)
            j = np.random.randint(0,N)
            S[i], S[j] = S[j], S[i]
        else:
            # randomly swap a subset of cities
            i = np.random.randint(0,N)
            j = np.random.randint(0,N)
            if i > j:
                i,j = j,i
            S[i:j] = S[i:j][::-1]

        #Annealing acceptance criterion
        if np.random.rand(1) < np.exp(-(energy(S) - energy(S0))/temp):
            S0 = S
        else:
            S = S0

        #Keep track of best path
        if energy(S0) > energy(S_best):
            S_best = S
    
    E = energy(S_best)

    return S_best, E

#===========================================
# Plots best path and coordinates
# input : S      : order of best path
#         E      : list of energies
#         p_type : string describing problem
#         coords : positions of stops, list of 2 or 3D arrays
def check(S,E,p_type,coords):
    if (p_type == 'random2D' or p_type == 'random3D'):
        plt.scatter(coords[:,0],coords[:,1],color='black')
        plt.plot(coords[S,0],coords[S,1],color='red')
        plt.show()
    elif (p_type == 'USA'):
        plt.scatter(coords[:,1],coords[:,0],color='black')
        plt.plot(coords[S,1],coords[S,0],color='red')
        plt.show()

    return

#===========================================
def main():

    parser = argparse.ArgumentParser(formatter_class=RawTextHelpFormatter)
    parser.add_argument("p_type",type=str,
                        help="problem name:\n"
                             "   random2D : a random assortment of cities in 2D space\n"
                             "   random3D : a random assortment of cities in 3D space\n"
                             "   USA      : the largest 'N' cities in the USA by population in 2D space\n"
                        )
    parser.add_argument("K",type=int,
                        help="max number of iterations")
    parser.add_argument("N",type=float,
                        help="number of cities to generate")


    args                     = parser.parse_args()
    p_type                   = args.p_type
    K                        = args.K
    N                        = args.N

    if (K < 5):
        parser.error("K must be larger than 5.")
    if (N < 4):
        parser.error("N must be larger than 3")

    coords  = init(p_type, N)

    S,E     = anneal_path(coords,K)

    check(S,E,p_type,coords)

#=============================================

main()