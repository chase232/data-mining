import random
import math
import operator
import collections
global cost, path

cost = [] # global table to cache results - cost[i] stores minimum cost of playing the game starting at cell i
path = [] #global table to store path leading to cheapest cost

def gaJumpIt(board):

    origBoard = board[0:]
    alleleCount = len(board)
    chromosomes = {}

    for i in range(0, alleleCount):
        chromosomes[i] = (generateInitialChromosome(alleleCount))

    cost1 = 0
    cost2 = 0

    costs = {}
    for i in range(0, alleleCount):
        costs[i] = getCost(board, chromosomes[i])

    for i in range(0,100):
        probs = []
        probsDic = {}
        sum1 = sum(costs.values())
        for i in range(0, alleleCount):
            probsDic[costs[i]/sum1] = chromosomes[i]
            

        probsDic2 = collections.OrderedDict(sorted(probsDic.items())) 

        chroms = []
        for item in probsDic2:
            chroms.append(probsDic2[item])

        child1, child2 = crossover(chroms[0], chroms[1])

        chroms.pop(0)
        chroms.pop(0)

        child1 = mutate(child1)
        child2 = mutate(child2)
        
        child1 = fixConsecutives(child1)
        child2 = fixConsecutives(child2)

        chroms.append(child1)
        chroms.append(child2)
        
    newCosts = {}
    for i in range(0, alleleCount):
        newCosts[getCost(board, chroms[i])] = chroms[i]

    newCosts2 = collections.OrderedDict(sorted(newCosts.items())) 

    smallest = []
    for item in newCosts2:
        smallest.append(newCosts2[item])

    smallestCost = []
    for key in newCosts:
        smallestCost.append(key)
    
    print("GA Solution")
    print("minimum cost", smallestCost[0])
    print("path showing indices of visited cells:", displayIndices(origBoard, smallest[0]))
    print("path showing contents of visited cells:", displayVisited(origBoard, smallest[0]))
    return smallestCost[0]
    
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
            #print("crossover")
            break
    # cut everyhing from right of index and swap with same in other parent
    if not crossOverIndex is None:
        child1 = selection1[0:crossOverIndex] + selection2[crossOverIndex:]
        child2 = selection2[0:crossOverIndex] + selection1[crossOverIndex:]
        return(child1, child2)
    else:
        return(selection1, selection2)

def getCost(board, alleles):
    #board = board[1:]
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
    f = open("input1.txt", "r") #input.txt
    accuracy = 0
    total = 0
    global cost, path
    for line in f:
        lyst = line.split() # tokenize input line, it also removes EOL marker
        lyst = list(map(int, lyst))
        cost = [0] * len(lyst) #create the cache table
        path = cost[:] # create a table for path that is identical to path
        min_cost = jumpIt(lyst)
        print("game board:", lyst)
        print("cost: ", min_cost)
        displayPath(lyst)
        print("___________________________")
        min_ga_cost = gaJumpIt(lyst)
    print("======================")
    print("GA Overall Accuracy", min_cost/min_ga_cost)

if __name__ == "__main__":
    main()
