"""
This document will contain the code for the classic traveling salesman problem, solved using simulated annealing.
"""
#===========================================
import argparse                  
from argparse import RawTextHelpFormatter
import numpy as np
import math
import matplotlib.pyplot as plt
from scipy.spatial.distance import cdist

import helper_functions as helper
#===========================================

#===========================================
# Returns model parameters depending on problem name
# input : p_type : string describing problem
#         N      : number of stops
# output: coords : positions of stops, list of 2 or 3D arrays
def init(p_type, N):
    if (p_type == 'circle'):
        coords = helper.circle_cities(int(N))
    elif (p_type == 'random2D'):
        coords = helper.rand_cities(int(N),2)
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
    coords = coords[S]

    for i in range(len(coords)-1):
        E += calculate_distance(coords[i-len(coords)+1][0], coords[i-len(coords)+1][1], coords[i][0], coords[i][1])

    return E

def calculate_distance(starting_x, starting_y, destination_x, destination_y):
    distance = math.hypot(destination_x - starting_x, destination_y - starting_y)  # calculates Euclidean distance (straight-line) distance between two points
    return distance

#===========================================
# Simulated annealing algorithm for traveling salesman problem
# input : coords : positions of stops, list of 2 or 3D arrays
#         delta  : stepsize to determine new trial state x'
#         K      : max number of iterations
# output: S      : list of best paths
#         E      : list of energies
def anneal_path(coords, K):
    N = len(coords)
    S0 = np.random.permutation(N)
    print(S0)
    S = S0
    S_best = S0

    for k in range(K):
        temp = 1 - (k)/K

        S_new = S

        u = np.random.rand(1)
        if u > 0.2:
            # randomly swap two cities
            i = np.random.randint(0,N)
            j = np.random.randint(0,N)
            S_new[i], S_new[j] = S[j], S[i]
        else:
            # randomly swap a subset of cities
            i = np.random.randint(0,N)
            j = np.random.randint(0,N)
            if i > j:
                i,j = j,i
            S_new[i:j] = S[i:j][::-1]

        #Annealing acceptance criterion
        if energy(S_new, coords) < energy(S, coords):
            S = S_new
        elif np.random.rand(1) < np.exp(-(energy(S_new, coords) - energy(S, coords))/temp):
            S = S_new
        else:
            S = S

        #Keep track of best path
        if energy(S, coords) < energy(S_best, coords):
            S_best = S
    
    E = energy(S_best, coords)

    return S_best, E

#===========================================
# Plots best path and coordinates
# input : S      : order of best path
#         E      : list of energies
#         coords : positions of stops, list of 2 or 3D arrays
def check(S,E,coords):
    plt.scatter(coords[:,0],coords[:,1],color='black', label='Cities')
    plt.plot(coords[S,0],coords[S,1],color='red', label='Best Path: E = %.2f' % (E))
    plt.legend(loc='upper right')
    plt.show()

    return

#===========================================
def main():

    parser = argparse.ArgumentParser(formatter_class=RawTextHelpFormatter)
    parser.add_argument("p_type",type=str,
                        help="problem name:\n"
                             "   circle   : 'N' cities arranged in a 'circle'\n"
                             "   random2D : a random assortment of cities in 2D space\n"
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
        parser.error("K must be larger than 5")
    if (N < 4):
        parser.error("N must be larger than 3")

    coords  = init(p_type, N)

    S,E     = anneal_path(coords,K)
    print(S)

    check(S,E,coords)

#=============================================

main()