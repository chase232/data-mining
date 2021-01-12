# Program:      HW4.py
# Developer:    Chase Dickerson
# Date:         11/14/2019
# Purpose:      Implment the K means algorithm 

from __future__ import division
import random
from collections import OrderedDict
import collections
import math
import time
import operator

global correct
correct = 0

def euclideanDistance(cluster, data):
    return math.sqrt(((float(cluster[0])-float(data[0]))**2)+(float(cluster[1])-float(data[1]))**2)

def clusterData(mean1, mean2, mean3, dataset):
    # Using euclidean distance with the data's x,y and mean's x,y
    clusters = {
        0: [],
        1: [],
        2: []
    }
    # Get distance from data to mean1,2,3 and add the data to the cluster
    # with the smallest distance.
    for data in dataset:
        distance = {
            0: euclideanDistance(mean1, data),
            1: euclideanDistance(mean2, data),
            2: euclideanDistance(mean3, data)
        }
        clusters[min(distance, key=distance.get)].append(data)
    return clusters

def calculateMean(clusters):
    mean1 = None
    mean2 = None
    mean3 = None

    # Loop through x and y and get new mean
    xTotal1 = 0
    yTotal1 = 0
    for data in clusters[0]:
        xTotal1 += float(data[0])
        yTotal1 += float(data[1])
    mean1 = [xTotal1/len(clusters[0]), yTotal1/len(clusters[0]), 0]

    # Loop through x and y and get new mean
    xTotal2 = 0
    yTotal2 = 0
    for data in clusters[1]:
        xTotal2 += float(data[0])
        yTotal2 += float(data[1])
    mean2 = [xTotal2/len(clusters[1]), yTotal2/len(clusters[1]), 1]

    # Loop through x and y and get new mean
    xTotal3 = 0
    yTotal3 = 0
    for data in clusters[2]:
        xTotal3 += float(data[0])
        yTotal3 += float(data[1])
    mean3 = [xTotal3/len(clusters[2]), yTotal3/len(clusters[2]), 2]
    return mean1, mean2, mean3
############  
def getAccuracy(clusters):
    # Loop through each cluster, tally if the data is in right cluster
    correct = 0
    total = 0
    for i in range(3):
        for data in clusters[i]:
            total += 1
            if int(data[2]) == i:
                correct += 1
    accuracy = int(correct) / int(total)
    print("Accuracy: " + str(accuracy*100) + "%")

def misclustered(clusters, i):
    incorrect = 0
    for data in clusters:
        if int(data[2]) != i:
            incorrect += 1
    return incorrect
#############
def calcAccuracy(clusters):
    # Print majority cluster, size, and incorrect
    
    # Loop through each cluster
    clusterDict = {
        '0': 0,
        '1': 0,
        '2': 0
    }
    # Loop through each cluster and get total
    for data in clusters:
        clusterDict[data[2]] += 1
    maxCluster = max(clusterDict.items(), key=operator.itemgetter(1))[0]
    numCorrect = clusterDict[maxCluster]
    global correct
    print("Cluster label", maxCluster)
    correct += numCorrect
    total = clusterDict['0'] + clusterDict['1'] + clusterDict['2']
    print("Number of objects misclustered in the cluster is", str(total - numCorrect))

def displayContent(clusters):
    for i in range(3):
        print("=====================")
        print("Cluster", i)
        print("Size of cluster", i, "is", len(clusters[i]))
        calcAccuracy(clusters[i])
        for data in clusters[i]:
            print("((" + str(data[0]) + ", " + str(data[1]) + "), " + str(data[2]) + ")")

def kMeans(dataset):
    # Get 3 random values for starting means
    print("Initial k means are")
    mean1 = dataset[random.randint(0,500)]
    mean2 = dataset[random.randint(0,500)]
    mean3 = dataset[random.randint(0,500)]
    print("mean[0] is ((" + str(mean1[0]) + ", " + str(mean1[1]) + "), " + str(mean1[2]) + ")")
    print("mean[1] is ((" + str(mean2[0]) + ", " + str(mean2[1]) + "), " + str(mean2[2]) + ")")
    print("mean[2] is ((" + str(mean3[0]) + ", " + str(mean3[1]) + "), " + str(mean3[2]) + ")")
    noMatch = True
    # Save previous means (may not be needed)
    prevMean1 = mean1
    prevMean2 = mean2
    prevMean3 = mean3
    # While means haven't changes from previous iter:
    while noMatch:
        # Organize the data into cluster with closest mean
        clusters = clusterData(mean1, mean2, mean3, dataset)

        # Recalculate the mean around the newly clustered data
            # Add all X's and Y's in each cluster to create:
            # (mean_x, mean_y, cluster)
        mean1, mean2, mean3 = calculateMean(clusters)
        # Check if these means are same as previous means
            # If so, break
            # Else, continue
        if mean1 == prevMean1 and mean2 == prevMean2 and mean3 == prevMean3:
            #print("Unchanged means: ", mean1, mean2, mean3)
            noMatch = False
        else:
            prevMean1 = mean1
            prevMean2 = mean2
            prevMean3 = mean3
    # Get accuracy here for output
        # Loop through all classes and see if they match the cluster they're in
    displayContent(clusters)
    print()
    print(str(correct/len(dataset)*100) + "%")
def main():
    dataset = []
    with open("synthetic_2D.txt", "r") as file:
        for line in file:
            dataset.append(line.split())
    kMeans(dataset)

if __name__ == "__main__":
    main()
