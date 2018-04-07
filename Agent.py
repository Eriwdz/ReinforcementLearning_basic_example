"""
    Agent.py created by mohit.badwal
    on 4/6/2018
    
"""
import numpy as np
import matplotlib.pyplot as plt

import random

import time

from data.Environment import GameEnvironment

# this is a random agent
totalReward = []
stateMatrices = []
x, y = GameEnvironment.s - 1, 0
count = 0
# directions = [0, 1, 2, 3]
# the qMatrix
qMatrix = np.zeros([GameEnvironment.s, GameEnvironment.s])

# randomly setting blockages in the matrix
li = []
while True:
    s1 = np.random.randint(0, GameEnvironment.s)
    s2 = np.random.randint(0, GameEnvironment.s)
    li.append((s1, s2))
    count = count + 1
    if count == (GameEnvironment.s // 2) + 1:
        break
for i in range(GameEnvironment.iterations):
    count = 0
    g = GameEnvironment(li, qMatrix=qMatrix)
    while True:
        # print(g.stateMatrix)
        count = count + 1
        direction = g.chooseMax((x, y))
        # print(directions)
        if count >= GameEnvironment.limit or direction == -1:
            print("Couldn't reach goal")
            g.clearMatrix()
            x, y = GameEnvironment.s - 1, 0
            break
        # direction = random.choice(directions)
        x, y = g.takeAction(direction, (x, y))
        print(direction, x, y)

        if x == 0 and y == GameEnvironment.s - 1:
            print("Reached Goal")
            stateMatrices.append(g.stateMatrix)
            totalReward.append(g.totalRewards)
            qMatrix = g.qMatrix
            g.clearMatrix()
            x, y = GameEnvironment.s - 1, 0
            break

# print(stateMatrices, totalReward)
print(qMatrix)
# print(qMatrix/np.max(qMatrix)*100)

# testing

for deer in range(20):
    x, y = GameEnvironment.s - 1, 0
    testMatrix = np.zeros([GameEnvironment.s, GameEnvironment.s])
    testMatrix[x][y] = 1
    count = 0
    g = GameEnvironment(li, qMatrix=qMatrix)
    i1, j1 = np.where(g.rewardMatrix == -5)
    testMatrix[GameEnvironment.s - 1][0] = 5
    for dope in list(zip(i1, j1)): testMatrix[dope] = 10
    print(testMatrix)
    while True:
        # print(g.stateMatrix)
        count = count + 1
        direction = g.chooseMax((x, y))
        # print(directions)
        if count >= GameEnvironment.limit or direction == -1:
            print("Couldn't reach goal")
            g.clearMatrix()
            x, y = GameEnvironment.s - 1, 0
            break
        # direction = random.choice(directions)
        x, y = g.takeAction(direction, (x, y))
        print(direction, x, y)
        testMatrix[x][y] = 5
        if x == 0 and y == GameEnvironment.s - 1:
            print("Reached Goal")
            stateMatrices.append(g.stateMatrix)
            totalReward.append(g.totalRewards)
            qMatrix = g.qMatrix
            g.clearMatrix()
            x, y = GameEnvironment.s - 1, 0
            break

    plt.matshow(testMatrix)
    plt.show()
