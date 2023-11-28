# simanneal
Semester-long project for PHYS 332 at UNC Chapel Hill on simulated annealing. (Prof: Dr. Fabian Heitsch)

Authors: Reece Clark, Hannah Perkins, Donovan Schlekat

## Files:

### global-maximum.py:
Finds the global maximum of a function using either a hill climber or a simulated annealing algorithm. Plots result.

Run in command line as

        python global-maximum.py -h
    
to see command line options.


### traveling-salesman.py: 
Solves the classic traveling salesman problem for a set of points either arranged in a "circle" or randomly distributed on a grid using simulated annealing. Plots result.

Run in command line as 

        python traveling-salesman.py -h
    
to see command line options.


### CityGridSimulation.py:
Finds the optimal route through a city grid or topographical map given a variety of different initial parameters. Plots result.

Run in command line as 
    
        python CityGridSimulation.py
    
To alter parameters, edit variables at the bottom of the file.


### StaticSimulation.py:
Solves the classic traveling salesman problem for a set of points randomly distributed on a grid using the brute force method or a greedy algorithm. Animates result. Plots result.

Run in command line as

        python StaticSimulation.py
    
To alter parameters, edit variables at the bottom of the file.


### helper_functions.py:
Auxiliary file. Used by traveling-salesman.py.
