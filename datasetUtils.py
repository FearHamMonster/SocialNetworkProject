import csv
from collections import defaultdict
from dataSetHierarchies import attributes_type
import numpy as np
import matplotlib.pyplot as plt

color = "r"

def plot_distribution_of_attr(distributions, attr):
    attr_distribution = distributions[attr]
    xvalues = list(attr_distribution.keys())
    yvalues = list(attr_distribution.values())
    plt.plot(xvalues, yvalues, c=color)

def get_distribution_from_dataset(noise = True, noise_factor = 20):
    distributions = {}
    for attribute in attributes_type.keys():
        distributions[attribute] = defaultdict(int)
           
    with open("csv/adult.csv", newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        counter = 0
        for row in reader:
            for attribute in row.keys():
                distributions[attribute][row[attribute]] += 1
            counter +=1
      
    
    for attribute in distributions.keys():
        for attribute_value in distributions[attribute].keys():
            if noise:
              if attributes_type[attribute] == "numerical":
                  continue  
            distributions[attribute][attribute_value] /= counter 

            
    #we want to add Laplacian noise to account for missing numerical values
    if noise:
        numerical_attributes = []
        for attribute in distributions.keys():
            if attributes_type[attribute] == "numerical":
                numerical_attributes.append(attribute)
                
        for attribute in numerical_attributes:
            attr_num_of_values = len(distributions[attribute].keys())
            for attribute_value in distributions[attribute].keys():
                #laplacian smoothing formula
                noised_probability = (distributions[attribute][attribute_value] + noise_factor) / ( noise_factor * attr_num_of_values +  counter)                                    
                distributions[attribute][attribute_value] = noised_probability 
    return distributions    

def get_distribution_from_graph(G):
    distributions = {}
    for attribute in attributes_type.keys():
        distributions[attribute] = defaultdict(int)

    for node in G.nodes:
        node_dict = G.nodes[node]["QIs"]
        for attribute in node_dict:
            distributions[attribute][node_dict[attribute]] += 1
        
    for attribute in distributions.keys():
        for attribute_value in distributions[attribute].keys():
            distributions[attribute][attribute_value] /= G.number_of_nodes()
    
def get_dataset_possible_values():
    attribute_name_to_values = defaultdict(list)
    with open("csv/adult.csv", newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            for attribute in row.keys():
                if attributes_type[attribute] == "numerical": #if it's numerical, save min and max as: num_attr : [min, max] 
                    if attribute_name_to_values[attribute] == []:
                         attribute_name_to_values[attribute] = [np.inf, 0]
                    if int(row[attribute]) < attribute_name_to_values[attribute][0]:
                        attribute_name_to_values[attribute][0] = int(row[attribute])
                    if int(row[attribute]) > attribute_name_to_values[attribute][1]:
                        attribute_name_to_values[attribute][1] = int(row[attribute])
                elif row[attribute] not in attribute_name_to_values[attribute]:
                    attribute_name_to_values[attribute].append(row[attribute])
    return attribute_name_to_values
    
    
def get_conditional_probabilities(base_attr, conditional_attr, bins=10):
    conditional_probabilities = [defaultdict(int) for _ in range(10)] 
    attr_count = [0] * 10
    with open("csv/adult.csv", newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            index = get_index(bins, int(row[base_attr]))
            if row[conditional_attr] not in conditional_probabilities[index]:     
                conditional_probabilities[index][row[conditional_attr]] = 1
            else: 
                conditional_probabilities[index][row[conditional_attr]] += 1

            attr_count[index] += 1

    for i in range(len(conditional_probabilities)):
        for cond_attr in conditional_probabilities[i].keys():                 
            if attr_count[i] != 0:
                conditional_probabilities[i][cond_attr] /= attr_count[i]
    return conditional_probabilities
                    

def get_index(bins, value):
    counter = bins
    index = 0
    while counter < value:
        counter += bins
        index += 1
    return index
    

distr = get_conditional_probabilities("age", "marital-status")
