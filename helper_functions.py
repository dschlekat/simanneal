"""
This document will contain helper functions for populating the 
coordinates of traveling salesman problems.
"""
#===========================================
import numpy as np
import math
#===========================================


#===========================================
# Random city coordinate generator
# Inputs:  cities     = number of desired cities generated
#          dimensions = number of dimensions (2 or 3)
# Outputs: coords     = array of n cities with 2/3 dimensions of random coordinates between 0 and 1
def rand_cities(cities, dimensions):
    dimensions = int(dimensions) #verify that dimensions is an integer

    if dimensions != 3 and dimensions != 2: #check that dimensions is valid
        raise Exception("Dimensions must be 2 or 3.")

    coords = np.zeros([cities,dimensions])

    for i in range(cities):
        rands = np.random.rand(dimensions)

        for j in range(dimensions):
            coords[i][j] = rands[j]

    return coords

#===========================================
# 'Circle' coordinate generator
# Inputs:  cities     = number of desired cities generated
# Outputs: coords     = array of n cities arranged in a 'circle'
def circle_cities(cities):
    # Define the radius of the regular polygon
    radius = 0.4

    # Calculate the angle between each city in radians
    angle = 2 * math.pi / cities

    # Generate coordinates for cities
    coords = np.array([(0.5 + radius * math.cos(i * angle), 0.5 + radius * math.sin(i * angle)) for i in range(cities)])

    return coords