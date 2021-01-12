"""
Program: assn1.py
Programmers: Chase Dickerson and Jacob Schaum
Description: This program creates a decision tree based off the data set Buy_computer.csv
"""

#Imports
import math
import itertools

#Global Variables
training_data = [] 

#Functions
#This function finds all of the main attributes 
def getAttributes():
    attributes = []
    input_data = training_data[0][0]
    for key in input_data:
        attributes.append(key)
    return attributes

#This function finds entropy
def entropy(attribute, dataset):
    entropy_sum = 0
    data_dict = {}    
    for data in dataset:
        if not data[0][attribute] in data_dict:
            data_dict[data[0][attribute]] = 1
        else:
            data_dict[data[0][attribute]] += 1
    data_max = len(dataset)
    for value in data_dict.values():
        entropy_sum = -1*(value/data_max*math.log(value/data_max, 2))
    return entropy_sum

#This function finds the classes of the data set
def getClasses():
    class_count = {}
    for data in training_data:
        if not data[1] in class_count:
            class_count[data[1]] = 1
        else:
            class_count[data[1]] += 1
    return class_count

#This function finds the values of the data set
def getValueData(root_node):
    attribute_values = []
    for data in training_data:
        # need array of all values, then build dict of counts for True/False for each value
        if data[0][root_node] not in attribute_values:
            attribute_values.append(data[0][root_node])
    val_data = {}
    for att in attribute_values:
        val_inner = {}
        for data in training_data:
            if data[0][root_node] == att:
                if not data[1] in val_inner:
                    val_inner[data[1]] = 1
                else:
                    val_inner[data[1]] += 1
                val_data[data[0][root_node]] = val_inner
    return val_data

#This is our actual id3 function
#   It is called recursivley to build decision tree
def id3(attributes, entropy_d, dataset):
      main_tree = {}
      # if data set class are all same, return class
      if len(dataset) > 0:
        first_element = dataset[0][1]
        all_same = False
        for data in dataset:
          if data[1] != first_element:
            all_same = False
            break
          else:
            all_same = True
        if all_same:
          return data[1]
        if attributes:
          min_entropy = math.inf
          test_attribute = ''
          for attribute in attributes:
              curr_entropy = entropy(attribute, dataset)
              if (entropy_d - curr_entropy) < min_entropy: 
                  min_entropy = (entropy_d - curr_entropy)
                  test_attribute = attribute
          branches = getValueData(test_attribute)
          tree = {}
          tree[None] = getMajorityClass(dataset)
          attributes.remove(test_attribute)
          for branch in branches.items():
            if len(branch[1]) == 1:
              tree[branch[0]] = next(iter(branch[1]))
            else: 
              new_training = []
              for data in dataset:
                if data[0][test_attribute] == branch[0]:
                  new_training.append(data)
              tree[branch[0]] = id3(attributes, entropy_d, new_training)
          main_tree[test_attribute] = tree
          return main_tree
        else:
          return getMajorityClass(dataset)
      else:
        return getMajorityClass(training_data)

#Finds the majority class
def getMajorityClass(dataset):
  class_counts = {}
  for data in dataset:
    if not data[1] in class_counts:
      class_counts[data[1]] = 1
    else:
      class_counts[data[1]] += 1
  max_class_val = 0
  max_class = ""
  for classes in class_counts.items():
      if classes[1] > max_class_val:
          max_class = classes[0]
          max_class_val = classes[1]
  return max_class

#Used to classify new data
def classify(tree, sample, expected):
  if type(tree) is str:
    print(tree)
    return
  first, second = next(iter(tree.keys())), next(iter(tree.values()))
  for key, vals in sample.items():
    if key == first:
      if vals in second:
        classify(second[vals], sample, expected)
      else:
        print(second[None])
        return
        
    elif len(sample) == 1:
        print(second[None])
        return

#Prepares the data from the file
def preprocessData():
    with open('Buy_computer.csv', "r") as file:
        for line in itertools.islice(file, 1, 1700):
            buy_computer = {}
            buy_computer["age"] = line.split(',')[1]
            buy_computer["income"] = line.split(',')[2]
            buy_computer["student"] = line.split(',')[3]
            buy_computer["credit_rating"] = line.split(',')[4]
            training_data.append(tuple((buy_computer, line.split(',')[5].strip())))

# Main function
def main():
    preprocessData()
    attributes = getAttributes()
    # Get class counts/entropy
    classes = getClasses()
    total_classes = 0
    entropy_d = 0
    for klass in classes.values(): # Calculate total number of classes (non-unique)
        total_classes += klass 
    for klass in classes.values(): # Calculate entropy for each unique class
        entropy_d += -1*(klass/total_classes*math.log(klass/total_classes, 2))
    tree = id3(attributes, entropy_d, training_data)
    for sample in training_data:
      classify(tree, sample[0], sample[1])
    print(tree)
if __name__ == "__main__":
  main()