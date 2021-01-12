import math

training_data = [
({'level':'Senior', 'lang':'Java', 'tweets':'no', 'phd':'no'}, False),
({'level':'Senior', 'lang':'Java', 'tweets':'no', 'phd':'yes'}, False),
({'level':'Mid', 'lang':'Python', 'tweets':'no', 'phd':'no'}, True),
({'level':'Junior', 'lang':'Python', 'tweets':'no', 'phd':'no'}, True),
({'level':'Junior', 'lang':'R', 'tweets':'yes', 'phd':'no'}, True),
({'level':'Junior', 'lang':'R', 'tweets':'yes', 'phd':'yes'}, False),
({'level':'Mid', 'lang':'R', 'tweets':'yes', 'phd':'yes'}, True),
({'level':'Senior', 'lang':'Python', 'tweets':'no', 'phd':'no'}, False),
({'level':'Senior', 'lang':'R', 'tweets':'yes', 'phd':'no'}, True),
({'level':'Junior', 'lang':'Python', 'tweets':'yes', 'phd':'no'}, True),
({'level':'Senior', 'lang':'Python', 'tweets':'yes', 'phd':'yes'}, True),
({'level':'Mid', 'lang':'Python', 'tweets':'no', 'phd':'yes'}, True),
({'level':'Mid', 'lang':'Java', 'tweets':'yes', 'phd':'no'}, True),
({'level':'Junior', 'lang':'Python', 'tweets':'no', 'phd':'yes'}, False)
] 

def getAttributes():
    attributes = []
    input_data = training_data[0][0]
    for key in input_data:
        attributes.append(key)
    return attributes

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

def getClasses():
    class_count = {}
    for data in training_data:
        if not data[1] in class_count:
            class_count[data[1]] = 1
        else:
            class_count[data[1]] += 1
    return class_count

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
            if data[0][root_node] is att:
                if not data[1] in val_inner:
                    val_inner[data[1]] = 1
                else:
                    val_inner[data[1]] += 1
                val_data[data[0][root_node]] = val_inner
    return val_data

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
          klass = data[1]
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

def getMajorityClass(dataset):
  true_count = 0
  false_count = 0
  for data in dataset:
    if data[1] == True:
      true_count += 1
    elif data[1] == False:
      false_count += 1
  if true_count > false_count:
    return True
  elif false_count > true_count:
    return False
  else:
    return True

def classify(tree, sample):
  if type(tree) is bool:
    print(tree)
    return
  first, second = next(iter(tree.keys())), next(iter(tree.values()))
  for key, vals in sample.items():
    if key == first:
      if vals in second:
        classify(second[vals], sample)
      else:
        print(second[None])
        return
    elif len(sample) == 1:
      print(second[None])
      return

def main():
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
    print(tree)
    test_samples = [
                    {"level": "Junior", "lang": "Java","tweets": "yes","phd": "no"}, 
                    {"level": "Junior", "lang": "Java","tweets": "yes","phd": "no"},
                    {"level": "Intern"},
                    {"level": "Senior"}
    ]
    for sample in test_samples:
      classify(tree, sample)

if __name__ == "__main__":
  main()