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
    radius = 0.4  # Adjust as needed

    # Calculate the angle between each city in radians
    angle = 2 * math.pi / cities

    # Generate coordinates for cities
    coords = np.array([(0.5 + radius * math.cos(i * angle), 0.5 + radius * math.sin(i * angle)) for i in range(cities)])

    return coords


#===========================================
# Random city coordinate generator
# Credit: List and lat/long distance conversion function found online at https://github.com/perrygeo/simanneal/blob/master/tests/helper.py
# License: 
    # Copyright (c) 2009, Richard J. Wagner <wagnerr@umich.edu>
    # Copyright (c) 2014, Matthew T. Perry <perrygeo@gmail.com>

    # Permission to use, copy, modify, and/or distribute this software for any
    # purpose with or without fee is hereby granted, provided that the above
    # copyright notice and this permission notice appear in all copies.

# Inputs:  cities     = number of desired cities generated
# Outputs: coords     = array of n random US cities with latitude/longitude
city_list = {
    'New York City': (40.72, 74.00),
    'Los Angeles': (34.05, 118.25),
    'Chicago': (41.88, 87.63),
    'Houston': (29.77, 95.38),
    'Phoenix': (33.45, 112.07),
    'Philadelphia': (39.95, 75.17),
    'San Antonio': (29.53, 98.47),
    'Dallas': (32.78, 96.80),
    'San Diego': (32.78, 117.15),
    'San Jose': (37.30, 121.87),
    'Detroit': (42.33, 83.05),
    'San Francisco': (37.78, 122.42),
    'Jacksonville': (30.32, 81.70),
    'Indianapolis': (39.78, 86.15),
    'Austin': (30.27, 97.77),
    'Columbus': (39.98, 82.98),
    'Fort Worth': (32.75, 97.33),
    'Charlotte': (35.23, 80.85),
    'Memphis': (35.12, 89.97),
    'Baltimore': (39.28, 76.62)
}

def USA_cities(cities: int):
    city_array = np.array(list(city_list.values()))

    if cities >= len(city_array):
        print('Maximum cities requested, returning all USA cities')
        cities = city_array
    else:
        cities = city_array[:cities]

    return cities

def distance(a, b):
    """Calculates distance between two latitude-longitude coordinates."""
    R = 3963  # radius of Earth (miles)
    lat1, lon1 = math.radians(a[0]), math.radians(a[1])
    lat2, lon2 = math.radians(b[0]), math.radians(b[1])
    return math.acos(math.sin(lat1) * math.sin(lat2) + math.cos(lat1) * math.cos(lat2) * math.cos(lon1 - lon2)) * R