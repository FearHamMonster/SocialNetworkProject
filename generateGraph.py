import pandas as pd
import csv
import networkx as nx
import GraphUtilities as utils
import random
import datasetUtils as dataset
from dataSetHierarchies import attributes_type

def get_dataset_rows_num():
    with open("csv/adult.csv", newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        return sum(1 for row in reader)
    
def assign_to_graph_random_rows(G, n, QI_attributes):
    rows_num = get_dataset_rows_num()
    rows_selected = random.sample(list(x for x in range(rows_num)), n)
    rows_selected = sorted(rows_selected)
    with open("csv/adult.csv", newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        counter = 0
        for i,row in enumerate(reader):
            if counter == n:
                break
            if i == rows_selected[0]:
                rows_selected.pop(0)
                for attribute in list(row.keys()):
                    if attribute not in QI_attributes:
                        row.pop(attribute)
                G.nodes[counter]["QIs"] = row
                counter += 1
        
def assign_to_graph_from_distribution(G, n, QI_attributes):
    nx.set_node_attributes(G, "*", "QIs")
    distributions = dataset.get_distribution_from_dataset()
    conditional_attributes = ["workclass", "marital-status"]
    conditional_attributes_dicts = []
    age_bins = 10
    for cond_attr in conditional_attributes:
        conditional_attributes_dicts.append(dataset.get_conditional_probabilities("age", cond_attr, bins=age_bins))
        
    for i in range(n):
        current_dict = {}
        for attribute in distributions.keys():
            if attribute in QI_attributes:
                #I take into consideration the empirical P(workclass | age) and P(marital-status | age)  
                if attribute in conditional_attributes:
                    cond_attr_index = conditional_attributes.index(attribute)
                    conditional_distribution = conditional_attributes_dicts[cond_attr_index]
                    dict_index = dataset.get_index(age_bins, int(current_dict["age"]))
                    cond_distribution_bin = conditional_distribution[dict_index]
                    attribute_values = list(cond_distribution_bin.keys())
                    probabilities = list(cond_distribution_bin.values()) 
                    current_dict[attribute] = random.choices(attribute_values, weights=probabilities)[0]
                else:
                    attribute_values = list(distributions[attribute].keys())
                    probabilities = list(distributions[attribute].values())
                    current_dict[attribute] = random.choices(attribute_values, weights=probabilities)[0]
        G.nodes[i]["QIs"] = current_dict
    return G

def assign_to_graph_random_values(G, n, QI_attributes):
    nx.set_node_attributes(G, "*", "QIs")
    possible_attr_values = dataset.get_dataset_possible_values()
    for i in range(n):
        current_dict = {}
        for attribute in QI_attributes:
            if attributes_type[attribute] == "numerical":
                current_dict[attribute] = random.randint(possible_attr_values[attribute][0], possible_attr_values[attribute][1])
            else:
                current_dict[attribute] = random.choice(possible_attr_values[attribute])
        G.nodes[i]["QIs"] = current_dict
    return G
    
        
#Generate a Erdos-Renyi graph, with the specified avarage degree
def generate_ErdosRenyi_graph(n, avarage_degree = 4,  from_dataset = True, random_values = False, seed=None, QI_attributes = list(attributes_type.keys())):
    probability = avarage_degree / n  
    if seed != None:
        random.seed(seed)
    G = nx.fast_gnp_random_graph(n, probability)
    if from_dataset:
        assign_to_graph_random_rows(G, n, QI_attributes)
    else:
        if random_values:
            assign_to_graph_random_values(G, n, QI_attributes)
        else:
            assign_to_graph_from_distribution(G, n, QI_attributes)
    return G


#Generate a Holme-Kim graph, that respects small world characteristics and power law distributions
#p = probability of adding a triangle after adding a random edge
#m = avarage number of edges per node
def generate_powerlaw_graph(p, m, n, from_dataset = True, random_values = False, seed = None,  QI_attributes = list(attributes_type.keys())):
    if seed != None:
        random.seed(seed)
    G = nx.powerlaw_cluster_graph(n, m, p, seed)
    if from_dataset:
        assign_to_graph_random_rows(G, n, QI_attributes)
    else:
        if random_values:
            assign_to_graph_random_values(G, n, QI_attributes)
        else:          
            assign_to_graph_from_distribution(G, n, QI_attributes)
    return G
    

