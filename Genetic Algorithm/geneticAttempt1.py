# Program:      HW3 Jump-It Game
# File:         assn3.py
# Developers:   Chase Dickerson and Jacob Schaum

import random
import math
global cost, path

cost = [] # global table to cache results - cost[i] stores minimum cost of playing the game starting at cell i
path = [] #global table to store path leading to cheapest cost

def gaJumpIt(board):

    origBoard = board[0:]
    alleleCount = len(board)

    # Create parents 1 and d
    parent1 = generateInitialChromosome(alleleCount)
    parent2 = generateInitialChromosome(alleleCount)

    # assign parents to selections
    selection1 = parent1
    selection2 = parent2
    
    cost1 = 0
    cost2 = 0

    for i in range(0,500):

        # Find two children using crossover
        child1, child2 = crossover(selection1, selection2)
        child1 = mutate(child1)
        child2 = mutate(child2)
        
        child1 = fixConsecutives(child1)
        child2 = fixConsecutives(child2)

        # Find the cost of each chromosome 
        parent1_cost = getCost(board,selection1)
        parent2_cost = getCost(board,selection2)
        child1_cost = getCost(board,child1)
        child2_cost = getCost(board,child2)
        total_cost = parent1_cost + parent2_cost + child1_cost + child2_cost

        # Find probabilty of each cost of Chromosome 
        parent1_chance = math.ceil(100*(parent1_cost/total_cost))
        parent2_chance = math.ceil(100*(parent2_cost/total_cost))
        child1_chance = math.ceil(100*(child1_cost/total_cost))
        child2_chance = math.ceil(100*(child2_cost/total_cost))
        
        # Find new set of chromosomes 
        if parent1_chance <= parent2_chance and parent1_chance <= child1_chance and parent1_chance <= child2_chance:
            selection1 = parent1
            cost1 = parent1_cost
        elif parent2_chance <= parent1_chance and parent2_chance <= child1_chance and parent2_chance <= child2_chance:
            selection1 = parent2
            cost1 = parent2_cost
        elif child1_chance <= parent1_chance and child1_chance <= parent2_chance and child1_chance <= child2_chance:
            selection1 = child1
            cost1 = child1_cost
        else:
            selection2 = child2
            cost2 = child2_cost

    print("GA Solution")
    if cost1 < cost2:
        print("minimum cost", cost1)
        print("path showing indices of visited cells:", displayIndices(origBoard, selection1))
        print("path showing contents of visited cells:", displayVisited(origBoard, selection1))
        return cost1
    else:
        print("minimum cost", cost2)
        print("path showing indices of visited cells:", displayIndices(origBoard, selection2))
        print("path showing contents of visited cells:", displayVisited(origBoard, selection2))
        return cost2
    
def displayIndices(board, selection):
    indices = ""
    for i in range(len(selection)):
        if selection[i] == 1:
            if indices == "":
                indices += str(i)
            elif i < len(selection):
                indices += " -> " + str(i)
    return indices

def displayVisited(board, selection):
    path = ""
    for i in range(len(selection)):
        if selection[i] == 1:
            if path == "":
                path += str(board[i])
            elif i < len(selection):
                path += " -> " + str(board[i])
    return path

def fixConsecutives(board):
    for i in range(len(board)):
        if i != 0 and board[i-1] == 0 and board[i] == 0:
            fixChance = random.random()
            if fixChance < 0.5:
                board[i-1] = 1
            else:
                board[i] = 1
    return board
    
def mutate(board):
    newBoard = board
    mutationProb = 0.02
    for i in range(len(newBoard)):
        mutateChance = random.random()
        if mutateChance < mutationProb:
            if newBoard[i] == 0:
                newBoard[i] = 1
            else:
                newBoard[i] = 0
    return newBoard

def crossover(selection1, selection2):
    # Check if previous element in index is 0 for two 0's in a row
    crossOverProb = 0.5
    crossOverIndex = None
    for i in range(len(selection1)):
        randomIndex = random.randint(1,len(selection1))    
        crossoverChance = random.random()
        if crossoverChance < crossOverProb:
            crossOverIndex = randomIndex
            break
    # cut everyhing from right of index and swap with same in other parent
    if not crossOverIndex is None:
        child1 = selection1[0:crossOverIndex] + selection2[crossOverIndex:]
        child2 = selection2[0:crossOverIndex] + selection1[crossOverIndex:]
        return(child1, child2)
    else:
        return(selection1, selection2)

def getCost(board, alleles):
    cost = 0
    for i in range(0, len(alleles)):
        if alleles[i] is 1:
            cost += board[i]
    return cost

def generateInitialChromosome(alleleCount):
    chromosome = []
    for i in range(alleleCount):
        # Ensures there's never 2 zeros in a row
        if i != 0 and chromosome[i-1] == 0:
            chromosome.append(1)
        else:
            if random.random() < 0.5:
                chromosome.append(0)
            else:
                chromosome.append(1)
    return chromosome

def jumpIt(board):
    #Bottom up dynamic programming implementation
    #board - list with cost associated with visiting each cell
    #return minimum total cost of playing game starting at cell 0
    
    n = len(board)
    cost[n - 1] = board[n - 1] #cost if starting at last cell
    path[n - 1] = -1 # special marker indicating end of path "destination/last cell reached"
    cost[n - 2] = board[n - 2] + board[n - 1] #cost if starting at cell before last cell
    path[n -2] = n - 1 #from cell before last, move into last cell
    #now fill the rest of the table
    for i in range(n-3, -1, -1):
        #cost[i] = board[i] + min(cost[i+1], cost[i+2])
        if cost[i +  1] < cost[i + 2]: # case it is cheaper to move to adjacent cell
            cost[i] = board[i] +  cost[i + 1]
            path[i] = i + 1 #so from cell i, one moves to adjacent cell
        else: 
            cost[i] = board[i] + cost[i + 2]
            path[i] = i + 2 #so from cell i, one jumps over cell
    return cost[0]
def displayPath(board):
    #Display path leading to cheapest cost - method displays indices of cells visited
    #path - global list where path[i] indicates the cell to move to from cell i
    cell = 0 # start path at cell 0
    print("path showing indices of visited cells:", end = " ")
    print(0, end ="")
    path_contents = "0" # cost of starting/1st cell is 0; used for easier tracing
    while path[cell] != -1: # -1 indicates that destination/last cell has been reached
        print(" ->", path[cell], end = "")
        cell = path[cell]
        path_contents += " -> " + str(board[cell])
    print()
    print("path showing contents of visited cells:", path_contents)

def main():
    f = open("input2.txt", "r") #input.txt
    global cost, path
    min_cost = 0
    min_ga_cost = 0
    for line in f:
        lyst = line.split() # tokenize input line, it also removes EOL marker
        lyst = list(map(int, lyst))
        cost = [0] * len(lyst) #create the cache table
        path = cost[:] # create a table for path that is identical to path
        min_cost += jumpIt(lyst)
        print("game board:", lyst)
        print("cost: ", min_cost)
        displayPath(lyst)
        print("___________________________")
        min_ga_cost += gaJumpIt(lyst)
    print("======================")
    print("GA Overall Accuracy", min_cost/min_ga_cost)

if __name__ == "__main__":
    main()
