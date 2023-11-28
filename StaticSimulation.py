import tkinter as tk
from tkinter import *
import random as rand
import math
import numpy as np
from sys import maxsize
from itertools import permutations

def getDistances(canvas, cities):
    n = len(cities)
    distances = np.zeros((n,n))

    for ind1, i in enumerate(cities):
        for ind2, j in enumerate(cities):
            x1c1, y1c1, x2c1, y2c1 = canvas.coords(cities[ind1])
            x1c2, y1c2, x2c2, y2c2 = canvas.coords(cities[ind2])

            xc1 = (x1c1 + x2c1) / 2
            yc1 = (y1c1 + y2c1) / 2
            xc2 = (x1c2 + x2c2) / 2
            yc2 = (y1c2 + y2c2) / 2

            distance = np.sqrt((xc1 - xc2) ** 2 + (yc1 - yc2) ** 2)
            distances[ind2,ind1] = distance

    return(distances)

def travellingsalesman1(c, order): #greedy
    global cost
    adj_vertex = 999
    min_val = 999
    visited[c] = 1
    indices = []
    order.append(c+1)

    for k in range(n):
        if (tsp_g[c][k] != 0) and (visited[k] == 0):
            if tsp_g[c][k] < min_val:
                min_val = tsp_g[c][k]
                adj_vertex = k

    if min_val != 999:
        cost = cost + min_val

    if adj_vertex == 999:
        adj_vertex = 0
        cost = cost + tsp_g[c][adj_vertex]
        return

    travellingsalesman1(adj_vertex, order)

def travellingsalesman2(graph, s, n, order): 
    vertex = []
    for i in range(n):
        if i != s:
            vertex.append(i)

    min_path = maxsize
    next_permutation = permutations(vertex)
    paths = list(np.zeros(n))

    for ind, i in enumerate(next_permutation):
        current_pathweight = 0
        k = s

        for j in i:
            current_pathweight += graph[k][j]
            k = j

        current_pathweight += graph[k][s]
        min_path = min(min_path, current_pathweight)
    print(paths)

    return min_path

def travellingsalesman3(objective, bounds, n_iterations, step_size, temp):
     # generate an initial point
     best = bounds[:, 0] + rand(len(bounds)) * (bounds[:, 1] - bounds[:, 0])
     # evaluate the initial point
     best_eval = objective(best)
     # current working solution
     curr, curr_eval = best, best_eval

     # run the algorithm
     for i in range(n_iterations):
         # take a step
         candidate = curr + np.randn(len(bounds)) * step_size
         # evaluate candidate point
         candidate_eval = objective(candidate)

     # check for new best solution
     if candidate_eval < best_eval:
         # store new best point
         best, best_eval = candidate, candidate_eval
         # report progress
         print('>%d f(%s) = %.5f' % (i, best, best_eval))
         # difference between candidate and current point evaluation
         diff = candidate_eval - curr_eval
         # calculate temperature for current epoch
         t = temp / float(i + 1)
         # calculate metropolis acceptance criterion
         metropolis = np.exp(-diff / t)

     # check if we should keep the new point
     if diff < 0 or rand() < metropolis:
         # store the new current point
         curr, curr_eval = candidate, candidate_eval

     return [best, best_eval]

def Cities(canvas,canvasSize,n):
    cities = []

    rr = 3

    for i in range(n):
        x = np.random.randint(canvasSize / 10, canvasSize - (canvasSize / 10))
        y = np.random.randint(canvasSize / 10, canvasSize - (canvasSize / 10))

        cities.append(canvas.create_oval(x - rr, y - rr, x + rr, y + rr, fill='black'))

    return cities

def createTraveler(canvas,canvasSize,cities):
    x1c, y1c, x2c, y2c = canvas.coords(cities[0])
    rr = 2
    x = (x1c + x2c) / 2
    y = (y1c + y2c) / 2

    traveler = canvas.create_oval(x - rr, y - rr, x + rr, y + rr, fill='red')

    return traveler

h = 1
def moveTraveler(canvas,traveler,cities,order,n):
    global h
    if h >= n:
        h = 0

    x1t, y1t, x2t, y2t = canvas.coords(traveler)
    xt = (x1t + x2t) / 2
    yt = (y1t + y2t) / 2
    dt = 1

    x1c, y1c, x2c, y2c = canvas.coords(cities[order[h]-1])
    xc = (x1c + x2c) / 2
    yc = (y1c + y2c) / 2

    dist = np.sqrt((xt - xc) ** 2 + (yt - yc) ** 2)

    if dist < 2:
        h += 1
        print(h)

    if dist != 0:
        xdir = (xc - xt) / dist
        ydir = (yc - yt) / dist
    else:
        xdir = 0
        ydir = 0

    xt += xdir * dt
    yt += ydir * dt

    canvas.create_oval(xt, yt, xt , yt, fill='red')

    canvas.coords(traveler, xt - 2, yt - 2, xt + 2, yt + 2)
    root.after(30, moveTraveler, canvas, traveler, cities, order, n)

# <editor-fold desc="Main Loop">

canvasSize = 200
n = 10

root = Tk()
root.geometry(f"{canvasSize}x{canvasSize}")

canvas = Canvas(root)
canvas.pack()

cities = Cities(canvas,canvasSize,n)
traveler = createTraveler(canvas,canvasSize,cities)

cost = 0 # initialize cost
visited = np.zeros(n, dtype=int) # set 0 for all locations since no locations have been visited
tsp_g = getDistances(canvas,cities) # create distances from each node
order = []

# travellingsalesman1(0, order)
travellingsalesman2(tsp_g, 0, n, order)
print(order)

root.after(30, moveTraveler, canvas, traveler, cities, order, n)

root.mainloop()
# </editor-fold>
