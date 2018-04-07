"""
    Environment.py created by mohit.badwal
    on 4/6/2018
    
"""
import random

import numpy as np


class GameEnvironment:
    s = 20
    iterations = s * 150
    limit = s * s

    def __init__(self, blockList, gamma=0.8, qMatrix=np.zeros([s, s])):
        # taking 2 matrices , one for  storing state and other or storing reward for that state
        self.stateMatrix = np.zeros([GameEnvironment.s, GameEnvironment.s])
        self.rewardMatrix = np.zeros([GameEnvironment.s, GameEnvironment.s])
        self.qMatrix = qMatrix
        self.gamma = gamma
        self.totalStepsTaken = 1
        self.totalRewards = 0
        self.blockList = blockList
        self.__intializeMatrix()

    def clearMatrix(self):
        self.stateMatrix = np.zeros([GameEnvironment.s, GameEnvironment.s])
        self.rewardMatrix = np.zeros([GameEnvironment.s, GameEnvironment.s])
        self.totalStepsTaken = 0
        self.totalRewards = 0

    def __intializeMatrix(self):
        # init all rewards to -2
        self.rewardMatrix.fill(-2)
        # init starting reward and not to go states
        count = 0
        for dope in self.blockList: self.rewardMatrix[dope] = -5
        self.rewardMatrix[0][GameEnvironment.s - 1] = 0
        self.rewardMatrix[GameEnvironment.s - 1][0] = -2
        print(self.rewardMatrix)
        # defining start and final state in state matrix
        self.stateMatrix[GameEnvironment.s - 1][0] = 1
        self.stateMatrix[0][GameEnvironment.s - 1] = -2

    def __availableActions(self, currState):
        x, y = currState
        directions = []

        try:
            if x - 1 < 0:
                pass
            elif self.stateMatrix[x - 1][y] == 0 or self.stateMatrix[x - 1][y] == -2:
                directions.append(0)
        except IndexError:
            pass
        try:
            if self.stateMatrix[x][y + 1] == 0 or self.stateMatrix[x][y + 1] == -2:
                directions.append(1)
        except IndexError:
            # directions.append(1)
            pass
        try:
            if self.stateMatrix[x + 1][y] == 0 or self.stateMatrix[x + 1][y] == -2:
                directions.append(2)
        except IndexError:
            # directions.append(2)
            pass
        try:
            if y - 1 < 0:
                pass
            elif self.stateMatrix[x][y - 1] == 0 or self.stateMatrix[x][y - 1] == -2:
                directions.append(3)
        except IndexError:
            # directions.append(3)
            pass
        return directions

    def __getCoordinates(self, direction, currState):
        x, y = currState
        if direction == 0:
            x, y = x - 1, y
        elif direction == 1:
            x, y = x, y + 1
        elif direction == 2:
            x, y = x + 1, y
        else:
            x, y = x, y - 1
        return x, y

    def chooseMax(self, currState):
        try:
            directions = self.__availableActions(currState)
            # print(directions)
            x, y = currState
            rewards = []
            directions1 = []
            coordinates = []
            for d in directions:
                x1, y1 = self.__getCoordinates(d, (x, y))
                reward = self.qMatrix[x1][y1]
                coordinates.append((x1, y1))
                rewards.append(reward)

            maxi = max(rewards)
            for i in range(len(rewards)):
                if maxi == rewards[i]:
                    directions1.append(directions[i])

            direction = random.choice(directions1)

            for j in range(len(rewards)):
                if direction == directions[j]:
                    self.__updateQMatrix(currState, rewards[j])

            return direction
        except ValueError:
            return -1

    def __updateQMatrix(self, currState, reward):
        x, y = currState
        self.qMatrix[x][y] = self.rewardMatrix[x][y] + self.gamma * reward

    def takeAction(self, direction, currState):
        # direction 0 is up , 1 is right , 2 is down and 3 is left
        x, y = currState
        self.totalStepsTaken = self.totalStepsTaken + 1
        try:
            if direction == 0:
                if x - 1 < 0:
                    raise IndexError
                self.stateMatrix[x - 1][y] = self.totalStepsTaken
                self.totalRewards = self.totalRewards + self.rewardMatrix[x - 1][y]
                x, y = x - 1, y
            elif direction == 1:
                self.stateMatrix[x][y + 1] = self.totalStepsTaken
                self.totalRewards = self.totalRewards + self.rewardMatrix[x][y + 1]
                x, y = x, y + 1
            elif direction == 2:
                self.stateMatrix[x + 1][y] = self.totalStepsTaken
                self.totalRewards = self.totalRewards + self.rewardMatrix[x + 1][y]
                x, y = x + 1, y
            else:
                if y - 1 < 0:
                    raise IndexError
                self.stateMatrix[x][y - 1] = self.totalStepsTaken
                self.totalRewards = self.totalRewards + self.rewardMatrix[x][y - 1]
                x, y = x, y - 1

        except IndexError:
            pass
            # self.stateMatrix[x][y] = self.totalStepsTaken
            # self.totalRewards = self.totalRewards + self.rewardMatrix[x][y]

        return x, y
