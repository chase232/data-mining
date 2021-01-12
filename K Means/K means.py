#!/usr/bin/env python3

import random
from collections import OrderedDict
import collections
import math
random.seed(12)

def euclideanDistance(cluster, data):
    return math.sqrt(pow(cluster-float(data[0]), 2) + pow(cluster-float(data[1]), 2))

def cluster(cluster1, cluster2, cluster3, dataset):
    clusterDict = OrderedDict()
    clusterDict[cluster1] = []
    clusterDict[cluster2] = []
    clusterDict[cluster3] = []
    cluster = [cluster1, cluster2, cluster3]
    for data in dataset:
        # Use euclidean distance to determine.
        distances = {
                        cluster1: euclideanDistance(float(cluster1), data),
                        cluster2: euclideanDistance(float(cluster2), data),
                        cluster3: euclideanDistance(float(cluster3), data)
                     }
        clusterDict[min(distances, key=distances.get)].append(data)
    return clusterDict

def recalculateMean(clusters):
    means = []
    for cluster in clusters.items():
        total = 0
        for data in cluster[1]:
            total += float(data[0])
        means.append(float(total)/len(cluster[1]))
    return means

def getAccuracy(clustered):
    sortedDict = collections.OrderedDict(sorted(clustered.items()))
    total = 0
    correct = 0
    for i in range(3):
        for value in sortedDict.values():
            for val in value:
                total += 1
                if int(val[2]) == i:
                    correct += 1
    print("Accuracy: ", float(correct)/float(total))

def kMeans(dataset):
    # Randomly select 3 elements as the mean of three clusters initially
    mean1 = dataset[random.randint(0, 199)]
    mean2 = dataset[random.randint(200, 349)]
    mean3 = dataset[random.randint(350, 500)]
    #print(mean1, mean2, mean3)
    # Loop until means dont change
    for i in range(100):
        print("mean1 is ", mean1)
        print("mean2 is ", mean2)
        print("mean3 is ", mean3)
        # Sort data to nearest mean
        #clustered = cluster(mean1, mean2, mean3, dataset)

        for data in dataset:
            point = data[0, 1]
            dist1 = math.sqrt(pow(mean1[0]-float(point[0]), 2) + pow(mean1[1]-float(point[1]), 2))
            dist2 = math.sqrt(pow(mean2[0]-float(point[0]), 2) + pow(mean2[1]-float(point[1]), 2))
            dist3 = math.sqrt(pow(mean3[0]-float(point[0]), 2) + pow(mean3[1]-float(point[1]), 2))

        # Recalculate mean of clusters
        newMeans = recalculateMean(clustered)
        newMeans.sort()
        #Get Accuracy
        getAccuracy(clustered)
        # Repeat until means dont change
        if mean1 != newMeans[0] and mean2 != newMeans[1] and mean3 != newMeans[2]: 
            mean1 = newMeans[0]
            mean2 = newMeans[1]
            mean3 = newMeans[2]
        else:
            print("Unchanged means: ", newMeans)
            break

def main():
    dataset = []
    with open("synthetic_2D.txt", "r") as file:
        for line in file:
            dataset.append(line.split())

    kMeans(dataset)

if __name__ == "__main__":
    main()
