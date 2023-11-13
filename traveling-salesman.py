"""
This document will contain the code for the classic traveling salesman problem, using simulated annealing.
"""
#===========================================
import argparse                  
from argparse import RawTextHelpFormatter
import numpy as np
import matplotlib.pyplot as plt

import helper_functions as helper
#===========================================

#===========================================
# coords = init(p_type)
# Returns model parameters depending on problem name
# input : p_type : string describing problem
#         N      : number of stops
# output: coords : positions of stops, list of 2 or 3D arrays
def init(p_type, N):
    if (p_type == 'random2D'):
        coords = helper.rand_cities(N,2)
    elif (p_type == 'random3D'):
        coords = helper.rand_cities(N,3)
    elif (p_type == 'USA'):
        coords = helper.USA_cities(N)
    elif (p_type == 'stars'):
        coords = helper.stars(N)
    else:
        raise Exception("[init]: invalid p_type = %s" % (p_type))

    return coords

#===========================================
def main():

    parser = argparse.ArgumentParser(formatter_class=RawTextHelpFormatter)
    parser.add_argument("p_type",type=str,
                        help="problem name:\n"
                             "   random2D : a random assortment of cities in 2D space\n"
                             "   random3D : a random assortment of cities in 3D space\n"
                             "   USA      : the largest 'N' cities in the USA by population in 2D space\n"
                             "   stars    : closest 'N' stars to the solar system in 3D space\n")
    parser.add_argument("K",type=int,
                        help="max number of iterations")
    parser.add_argument("delta",type=float,
                        help="stepsize to determine new trial state x'")


    args                     = parser.parse_args()
    p_type                   = args.p_type
    K                        = args.K
    delta                    = args.delta

    if (K < 100):
        parser.error("K must be larger than 100.")
    if (delta <= 0.0):
        parser.error("delta must be larger than zero")

    coords  = init(p_type)

    X,E     = anneal_path(coords,delta,K)

    check(X,E,p_type,coords)

#=============================================

main()