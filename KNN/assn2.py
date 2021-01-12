#!/usr/bin/env python3

# Program:      KNN algorithm
# Developer:    Chase Dickerson
# Date:         10/07/2019

import sys
import csv
import math
import operator

#Global Variables
trainingData = []
testData = []

# Reads the training and test data in
def preprocessData(trainingFile, testFile):
    with open(trainingFile, 'r') as csvFile1:
        trainingLines = csv.reader(csvFile1)
        dataSet1 = list(trainingLines)
        global trainingData
        for x in range(len(dataSet1)):
            trainingData.append(dataSet1[x])

    with open(testFile, 'r') as csvFile:
        testLines = csv.reader(csvFile)
        dataSet2 = list(testLines)
        global testData
        for x in range(len(dataSet2)):
            testData.append(dataSet2[x])

# Ecludian distance is used to find the distance between 2 points
def ecludianDistance(p, q, l):
    distSum = 0
    for x in range(l):
        distSum += pow((int(p[x + 1]) - int(q[x + 1])), 2)
    return math.sqrt(distSum)

# KNN algorithm used to predict a class
def kkn(trainingData, K, test):
    neighbors = []

    # Finds K closest neighbors
    for d in range(len(trainingData)):
        if len(neighbors) <= K:
            neighbors.append(trainingData[d])
        else:
            for n in neighbors:
                if ecludianDistance(test, n, len(test) - 1) >= ecludianDistance(test, trainingData[d], len(test) - 1):
                    neighbors.remove(n)
                    neighbors.append(trainingData[d])

    # Weighted voting 
    distances = []
    for n in neighbors:
        distance = 1 / pow(ecludianDistance(test, n, len(test) - 1), 2)
        distances.append(distance)

    # Voting for the predicted class using weights
    votes = {}
    distanceCount = 0
    for n in range(len(neighbors)):
        response = neighbors[n][0]
        if response in votes:
            votes[response] += distances[distanceCount]
        else:
            votes[response] = distances[distanceCount]
        distanceCount = distanceCount + 1

    predictedClass = max(votes.items(), key=operator.itemgetter(1))[0]
    return predictedClass

# Prints data on the accuracy
def getAccuracyData(computedClasses, testData):
	correct = 0 
	incorrect = 0
	for x in range(len(testData)):
		if testData[x][0] == computedClasses[x]:
			correct += 1
		else:
			incorrect += 1
	  
	accuracyRate = (correct/float(len(testData))) * 100.0
	print('Accuracy rate: ' + repr(accuracyRate))
	print('Number of misclassified test samples: ' + repr(incorrect)) 
	print('Total number of test samples: ' + repr(len(testData)))

def main():
    preprocessData('MNIST_train.csv', 'MNIST_test.csv')

    trainingData.pop(0)     #Removing headers
    testData.pop(0)         #Removing headers
    predictedClasses = []

    numberOfClasses = []
    for x in range(len(testData)):
        c = testData[x][0]
        if c not in numberOfClasses:
            numberOfClasses.append(c)

    K = math.floor(math.sqrt(len(numberOfClasses)))

    print("K = " + repr(K))
    for x in range(len(testData)):
        klass = kkn(trainingData, K, testData[x])
        predictedClasses.append(klass)
        print('Desired class: ' + repr(testData[x][0]) + ', computed class: ' + repr(klass))
    getAccuracyData(predictedClasses, testData)

if __name__ == "__main__":
  main()

