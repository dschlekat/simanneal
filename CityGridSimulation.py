import tkinter as tk
from tkinter import *
import random as rand
import math
import numpy as np
from sys import maxsize
from itertools import permutations
import time
from PIL import Image, ImageTk
import matplotlib.pyplot as plt

def listCopy(list):
    newlist = []
    for i in list:
        newlist.append(i)
    return newlist

def rgbtohex(r,g,b):
    return f'#{r:02x}{g:02x}{b:02x}'

def startCity(canvas,canvasSize):
    rr = 3

    x = 15
    y = canvasSize - 15

    city1 = canvas.create_oval(x - rr, y - rr, x + rr, y + rr, fill='red')

    return city1

def endCity(canvas, canvasSize):
    rr = 3

    x = canvasSize - 15
    y = 15

    city2 = canvas.create_oval(x - rr, y - rr, x + rr, y + rr, fill='red')

    return city2

def createNodesChaotic(canvas, city1, city2, canvasSize, n):
    rr = 4

    xs1,ys1,xs2,ys2 = canvas.coords(city1)
    xe1,ye1,xe2,ye2 = canvas.coords(city2)

    xs = (xs1 + xs2) / 2
    ys = (ys1 + ys2) / 2

    xe = (xe1 + xe2) / 2
    ye = (ye1 + ye2) / 2

    xnodes = np.linspace(1,abs(xs-xe),n)
    ynodes = np.linspace(1, abs(ys - ye), n)

    nodes = np.zeros((n,n))
    nodeCosts = []

    for ind1, i in enumerate(xnodes):
        for ind2, j in enumerate(ynodes):
            cost = int(np.random.rand(1) * 255)
            nodes[ind1, ind2] = canvas.create_oval(i + 15 - rr, j + 15 - rr, i + 15 + rr, j + 15 + rr, fill=rgbtohex(1,cost,1))
            nodeCosts.append(cost/255)

    return nodes, nodeCosts

def createNodesControl(canvas, city1, city2, canvasSize, n):
    rr = 4

    xs1,ys1,xs2,ys2 = canvas.coords(city1)
    xe1,ye1,xe2,ye2 = canvas.coords(city2)

    xs = (xs1 + xs2) / 2
    ys = (ys1 + ys2) / 2

    xe = (xe1 + xe2) / 2
    ye = (ye1 + ye2) / 2

    xnodes = np.linspace(1,abs(xs-xe),n)
    ynodes = np.linspace(1, abs(ys - ye), n)

    nodes = np.zeros((n,n))
    nodeCosts = []

    for ind1, i in enumerate(xnodes):
        for ind2, j in enumerate(ynodes):
            print(i/j,i,j,ind1,ind2)
            # cost = int(((ind2+ind1)/(2*n)) * 255)
            if ind1 > 4 and ind1 < 15 and ind2 > 4 and ind2 < 15:
                cost = 255
            else:
                cost = 1
            nodes[ind1, ind2] = canvas.create_oval(i + 15 - rr, j + 15 - rr, i + 15 + rr, j + 15 + rr, fill=rgbtohex(1,cost,1))
            nodeCosts.append(cost/255)

    return nodes, nodeCosts

def initialPath(nodes,nodeCosts,n):
    startNode = nodes[-1,0]
    endNode = nodes[0,-1]

    path = [startNode]
    index = startNode

    for i in range(n-1):
        index += 1
        path.append(index)
        index -= n
        path.append(index)

    totcost = 0

    for ind, i in enumerate(path):
        totcost += nodeCosts[int(i - 3)]

    return path

def pathCost(path,nodeCosts):
    totcost = 0

    for i in path:
        totcost += nodeCosts[int(i-3)]

    return totcost

def optimizePath(path,nodes,nodeCosts,n):
    path = path[1:-1]
    oldPath = listCopy(path)

    costs = []
    iters = 1000
    when = []
    eff = 0

    for i in range(iters):
        nodeSwap = np.random.randint(0, ((n - 2) * 2))
        direc = np.random.randint(0, 2)

        # if direc == 0 and path[nodeSwap] > n + 1 and ((path[nodeSwap] + 1) % n) != 0:
        #     if path[nodeSwap - 1] + 1 == path[nodeSwap] and path[nodeSwap + 1] + n == path[nodeSwap]:
        #         path[nodeSwap] -= (n+1)
        #
        # elif direc == 1 and path[nodeSwap] < n * n - 2 and ((path[nodeSwap] + 2) % n) != 0:
        #     if path[nodeSwap - 1] - n == path[nodeSwap] and path[nodeSwap + 1] - 1 == path[nodeSwap]:
        #         path[nodeSwap] += (n+1)

        if direc == 0 and path[nodeSwap] > n + 1:
            if path[nodeSwap - 1] + 1 == path[nodeSwap] and path[nodeSwap + 1] + n == path[nodeSwap]:
                path[nodeSwap] -= (n+1)
                eff += 1

        elif direc == 1 and path[nodeSwap] < n * n - 2:
            if path[nodeSwap - 1] - n == path[nodeSwap] and path[nodeSwap + 1] - 1 == path[nodeSwap]:
                path[nodeSwap] += (n+1)
                eff += 1

        currPath = listCopy(path)

        if pathCost(currPath,nodeCosts) < pathCost(oldPath,nodeCosts):
            oldPath = listCopy(currPath)
            # drawPath(canvas,oldPath)
        else:
            val = np.random.rand(1)
            if val > i/iters:
                oldPath = listCopy(currPath)
                # drawPath(canvas, oldPath)
            else:
                path = listCopy(oldPath)

        if i in when:
            costs.append(pathCost(path,nodeCosts))
            drawPath(canvas,oldPath,city1,city2,i/iters)

    print(eff)
    print(costs)
    plt.plot(when[:-1],costs,color='red',marker='o')
    plt.xlabel("Path Modifications")
    plt.ylabel("Cost")
    plt.title("Optimization")
    # plt.show()
    return path

def drawPath(canvas,path,city1,city2,iters):

    color = rgbtohex(int(iters * 255),1,int((1-iters) * 255))

    w = 2
    for ind in range(len(path)-1):
        xs1, ys1, xs2, ys2 = canvas.coords(int(path[ind]))
        xe1, ye1, xe2, ye2 = canvas.coords(int(path[ind+1]))

        xs = (xs1 + xs2) / 2
        ys = (ys1 + ys2) / 2

        xe = (xe1 + xe2) / 2
        ye = (ye1 + ye2) / 2

        canvas.create_rectangle(xs-w,ys-w,xe+w,ye+w,fill=color,outline=color)

    xs1, ys1, xs2, ys2 = canvas.coords(city2)
    xe1, ye1, xe2, ye2 = canvas.coords(int(path[0]))

    xs = (xs1 + xs2) / 2
    ys = (ys1 + ys2) / 2

    xe = (xe1 + xe2) / 2
    ye = (ye1 + ye2) / 2

    canvas.create_rectangle(xs-w, ys-w, xe+w, ye+w, fill=color, outline=color)

    xs1, ys1, xs2, ys2 = canvas.coords(int(path[-1]))
    xe1, ye1, xe2, ye2 = canvas.coords(city1)

    xs = (xs1 + xs2) / 2
    ys = (ys1 + ys2) / 2

    xe = (xe1 + xe2) / 2
    ye = (ye1 + ye2) / 2

    canvas.create_rectangle(xs-w, ys-w, xe+w, ye+w, fill=color, outline=color)

canvasSize = 600
n = 5

root = Tk()

canvas = Canvas(height=canvasSize,width=canvasSize)
canvas.pack()

city1 = startCity(canvas, canvasSize)
city2 = endCity(canvas, canvasSize)
nodes, nodeCosts = createNodesChaotic(canvas,city1,city2,canvasSize,n)
path = initialPath(nodes,nodeCosts,n)
initialpathCost = pathCost(path,nodeCosts)

path = optimizePath(path,nodes,nodeCosts,n)
drawPath(canvas,path,city1,city2,1)
finalpathCost = pathCost(path,nodeCosts)

print(initialpathCost,finalpathCost)

root.mainloop()