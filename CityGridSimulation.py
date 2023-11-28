import tkinter as tk
from tkinter import *
import numpy as np
import time
import matplotlib.pyplot as plt


def listCopy(list):
    newlist = []
    for i in list:
        newlist.append(i)
    return newlist


# convert rgb to hexadecimal
def rgbtohex(r, g, b):
    return f'#{r:02x}{g:02x}{b:02x}'


# creates the starting city
def boundaryNode(canvas, canvasSize, l):
    rr = 10  # radius of boundary node

    if l == 0:  # create bottom left node
        x = 15
        y = canvasSize - 15
    if l == 1:  # create top right node
        x = canvasSize - 15
        y = 15

    boundaryNode = canvas.create_oval(x - rr, y - rr, x + rr, y + rr, fill='red')  # create boundary node

    return boundaryNode  # return boundary node


# creates nodes for the chaotic model
def createNodesChaotic(canvas, city1, city2, canvasSize, n):
    rr = 5  # radius of nodes

    xs1, ys1, xs2, ys2 = canvas.coords(city1)  # get coordinates of the start node
    xe1, ye1, xe2, ye2 = canvas.coords(city2)  # get coordinates of the end node

    xs = (xs1 + xs2) / 2  # true x coordinate of start node
    ys = (ys1 + ys2) / 2  # true y coordinate of start node

    xe = (xe1 + xe2) / 2  # true x coordinate of end node
    ye = (ye1 + ye2) / 2  # true y coordinate of end node

    xnodes = np.linspace(1, abs(xs - xe), n)  # get x coordinates to distribute the nodes across the canvas
    ynodes = np.linspace(1, abs(ys - ye), n)  # get y coordinates to distribute the nodes across the canvas

    nodes = np.zeros((n, n))  # create the matrix of nodes
    nodeCosts = []  # initialize the list of node costs

    for ind1, i in enumerate(xnodes):  # for x values of nodes
        for ind2, j in enumerate(ynodes):  # for y values of nodes
            cost = int(np.random.rand(1) * 255)  # create a cost
            nodes[ind1, ind2] = canvas.create_oval(i + 15 - rr, j + 15 - rr, i + 15 + rr, j + 15 + rr,
                                                   fill=rgbtohex(cost, cost, cost))  # create node with cost color
            nodeCosts.append(cost / 255)  # set the cost

    return nodes, nodeCosts  # return the node matrix and cost of nodes


# creates nodes for the control model
def createNodesControl(canvas, city1, city2, canvasSize, n):
    rr = 10  # radius of nodes

    xs1, ys1, xs2, ys2 = canvas.coords(city1)  # get coordinates of the start node
    xe1, ye1, xe2, ye2 = canvas.coords(city2)  # get coordinates of the end node

    xs = (xs1 + xs2) / 2  # true x coordinate of start node
    ys = (ys1 + ys2) / 2  # true y coordinate of start node

    xe = (xe1 + xe2) / 2  # true x coordinate of end node
    ye = (ye1 + ye2) / 2  # true y coordinate of end node

    xnodes = np.linspace(1, abs(xs - xe), n)  # get x coordinates to distribute the nodes across the canvas
    ynodes = np.linspace(1, abs(ys - ye), n)  # get y coordinates to distribute the nodes across the canvas

    nodes = np.zeros((n, n))  # create the matrix of nodes
    nodeCosts = []  # initialize the list of node costs

    for ind1, i in enumerate(xnodes):
        for ind2, j in enumerate(ynodes):
            print(i / j, i, j, ind1, ind2)
            cost = int(((ind2 + ind1) / (2 * n)) * 255)
            # if ind1 > 4 and ind1 < 15 and ind2 > 4 and ind2 < 15:
            #     cost = 255
            # else:
            #     cost = 1
            nodes[ind1, ind2] = canvas.create_oval(i + 15 - rr, j + 15 - rr, i + 15 + rr, j + 15 + rr,
                                                   fill=rgbtohex(cost, cost, cost))
            nodeCosts.append(cost / 255)

    return nodes, nodeCosts  # return the node matrix and cost of nodes


# creates nodes for the valley model
def createNodesValley(canvas, city1, city2, canvasSize, n):
    rr = 33  # radius of nodes

    xs1, ys1, xs2, ys2 = canvas.coords(city1)  # get coordinates of the start node
    xe1, ye1, xe2, ye2 = canvas.coords(city2)  # get coordinates of the end node

    xs = (xs1 + xs2) / 2  # true x coordinate of start node
    ys = (ys1 + ys2) / 2  # true y coordinate of start node

    xe = (xe1 + xe2) / 2  # true x coordinate of end node
    ye = (ye1 + ye2) / 2  # true y coordinate of end node

    xnodes = np.linspace(1, abs(xs - xe), n)  # get x coordinates to distribute the nodes across the canvas
    ynodes = np.linspace(1, abs(ys - ye), n)  # get y coordinates to distribute the nodes across the canvas

    nodes = np.zeros((n, n))  # create the matrix of nodes
    # initialize the list of node costs
    nodeCosts = [1, 1, 1, .75, .5, .25, 0, 0, 0, 0,
                 1, 1, .75, .75, .5, .25, 0, .25, .25, 0,
                 1, .75, .5, .5, .25, .25, 0, .25, .25, 0,
                 .75, .5, .25, .25, 0, 0, 0, .25, .25, 0,
                 .5, .25, 0, 0, 0, .25, .25, .5, .25, 0,
                 .25, 0, 0, .25, .25, .5, .5, .25, .25, 0,
                 .25, 0, .25, .5, .5, .5, .25, 0, 0, 0,
                 .25, 0, .25, .25, .25, .25, .25, 0, .25, .25,
                 .25, 0, .25, 0, 0, 0, 0, 0, .25, .5,
                 0, 0, 0, 0, .25, .25, .25, .25, .5, .75]

    h = 0
    for ind1, i in enumerate(xnodes):
        for ind2, j in enumerate(ynodes):
            nodes[ind1, ind2] = canvas.create_oval(i + 15 - rr, j + 15 - rr, i + 15 + rr, j + 15 + rr,
                                                   fill=rgbtohex(1, int(nodeCosts[h] * 255), 1))
            h += 1

    return nodes, nodeCosts  # return the node matrix and cost of nodes


# create the initial path
def initialPath(nodes, nodeCosts, n):
    startNode = nodes[-1, 0]  # get the first node
    endNode = nodes[0, -1]  # get the last node

    path = [startNode]  # start the path as a list with the first node
    index = startNode  # get the index as the first node

    # create a loop to gather all nodes needed and append them
    for i in range(n - 1):
        index += 1
        path.append(index)
        index -= n
        path.append(index)

    return path  # return the initial path


# create a function to return the cost of some path
def pathCost(path, nodeCosts):
    totcost = 0  # initialize the total cost

    # create a loop to add the cost element of every path element
    for i in path:
        totcost += nodeCosts[int(i - 3)]

    return totcost  # return the total cost of the path


# create a function to update the path nodes
def optimizePath(path, nodeCosts, n, iters, npaths):
    oldPath = listCopy(path)  # initialize the old path
    bestPath = path

    costs = []  # initialize the list of costs
    when = list(np.linspace(1, iters, npaths + 1, dtype="int"))  # create a list of which iterations to plot the cost of
    eff = 0  # initialize the number of effective path modifications
    smallest = path[int(n / 2)]
    largest = path[int(n / 2)]

    # create a loop for the number of iterations chosen
    for i in range(iters):
        print(str(round((i / iters) * 100, 3)) + "%")
        nodeSwap = np.random.randint(0, ((n - 2) * 2) + 2)  # randomly choose a node to be attempted to be modified
        direc = np.random.randint(0, 2)  # choose which direction to modify the node

        oldNode = path[nodeSwap]  # set the old node

        # create statements to maintain a proper path and update the path
        if direc == 0 and path[nodeSwap] > n + 1:
            if path[nodeSwap - 1] + 1 == path[nodeSwap] and path[nodeSwap + 1] + n == path[nodeSwap]:
                path[nodeSwap] -= (n + 1)
                eff += 1

        elif direc == 1 and path[nodeSwap] < n * n - 2:
            if path[nodeSwap - 1] - n == path[nodeSwap] and path[nodeSwap + 1] - 1 == path[nodeSwap]:
                path[nodeSwap] += (n + 1)
                eff += 1

        # test if the path modification lowered the cost
        if nodeCosts[int(path[nodeSwap] - 3)] < nodeCosts[int(oldNode - 3)]:
            oldPath = listCopy(path)  # set the old path as the current path
            bestPath = path  # set the best path as the path


        else:
            # choose a random value
            val = np.random.rand(1)

            # give the path the possibility to still be modified
            if val > i / iters:
                oldPath = listCopy(path)
            else:
                path = listCopy(oldPath)

        # create a statement to add to the list of which iterations to be plotted
        if i in when:
            costs.append(pathCost(path, nodeCosts))
            drawPath(canvas, oldPath, i / iters, 1)

    # plot the optimizations
    plt.plot(when[:-1], costs, color='green', marker='o')
    plt.xlabel("Path Modifications")
    plt.ylabel("Cost")
    plt.title("Optimization")
    plt.show()

    return bestPath  # return the best path


# create a function to draw the path
def drawPath(canvas, path, iters, params):
    if params == 1:
        color = rgbtohex(int(iters * 255), 1, int((1 - iters) * 255))  # get the color of the path
    elif params == 0:
        color = 'orange'

    w = 0.7  # create the width of the path blocks

    # create a loop to draw the path blocks
    for ind in range(len(path) - 1):
        xs1, ys1, xs2, ys2 = canvas.coords(int(path[ind]))
        xe1, ye1, xe2, ye2 = canvas.coords(int(path[ind + 1]))

        xs = (xs1 + xs2) / 2
        ys = (ys1 + ys2) / 2

        xe = (xe1 + xe2) / 2
        ye = (ye1 + ye2) / 2

        canvas.create_rectangle(xs - w, ys - w, xe + w, ye + w, fill=color, outline=color)


# set the canvas size, size of grid, number of paths to plot, size of iterations to map, and number of runs for each
# of those iterations
canvasSize = 800
n = 40
npaths = 10
trials = [100000]
runs = 1

root = Tk()

canvas = Canvas(height=canvasSize, width=canvasSize)
canvas.pack()

city1 = boundaryNode(canvas, canvasSize, 0)  # create the first node
city2 = boundaryNode(canvas, canvasSize, 1)  # create the last node

nodes, nodeCosts = createNodesChaotic(canvas, city1, city2, canvasSize, n)
# nodes, nodeCosts = createNodesControl(canvas, city1, city2, canvasSize, n)
# nodes, nodeCosts = createNodesValley(canvas,city1,city2,canvasSize,n)

path = initialPath(nodes, nodeCosts, n)  # create the initial path
initialpathCost = pathCost(path, nodeCosts)  # find the initial path cost

startTime = time.time()  # start time
allx = []
ally = []
for j in range(runs):
    deltaCosts = []
    for ind, i in enumerate(trials):
        currpath = optimizePath(path, nodeCosts, n, int(i), npaths)  # run the optimization function

        drawPath(canvas, currpath, 1, 1)  # draw the path
        finalpathCost = pathCost(currpath, nodeCosts)  # find the final cost
        deltaCosts.append(finalpathCost - initialpathCost)
    for ind, i in enumerate(deltaCosts):
        allx.append(np.log10(trials[ind]))
        ally.append(deltaCosts[ind])
    plt.scatter(np.log10(trials), deltaCosts, color='red')
    plt.xlabel("Total number of iterations (log10)")
    plt.ylabel("Change in cost")
    plt.title("Relationship between more iterations and cost")

m, b = np.polyfit(allx, ally, 1)

xvals = np.linspace(min(allx), max(allx), 2)
yvals = (m * xvals) + b

plt.plot(xvals, yvals, color='black')
plt.show()
endTime = time.time()  # end time

# print details
print("Computation time: " + str(round(endTime - startTime, 3)) + " seconds" +
      "\nInitial cost: " + str(round(initialpathCost, 4)) +
      "\nFinal cost: " + str(round(finalpathCost, 4)) +
      "\nChange in cost: " + str(round(finalpathCost - initialpathCost, 4)) +
      "\nChange in cost per 10 times iterations: " + str(m))

root.mainloop()
