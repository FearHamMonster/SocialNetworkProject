import argparse
import generateGraph as graphgen
import csv
import logging
import random
import anon
from dataSetHierarchies import attributes_type, gen_trees
from datasetUtils import get_dataset_possible_values

#equivalent of "COUNT FROM TABLE WHERE attr = target_num"
def count_nodes_that_satisfy_query(attr, target_num, G):
    counter = 0
    for node in G.nodes:
        if int(G.nodes[node]["QIs"][attr]) == target_num:
            counter+=1
    return counter

def count_nodes_that_satisfy_query_masked(attr, target_num, masked_G):
    counter = 0
    for node in masked_G.nodes:
        min, max = masked_G.nodes[node]["QIs"][attr]        
        if target_num <= max and target_num>=min:
            counter+=1
    return counter
    


def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--real-dataset', type=bool, default=True, help="a real dataset is gonna be used (if false, a synthetic one will be constructed with the same distribution as the first one)")
    parser.add_argument('--random-values', type=bool, default=False, help="values of attributes will be chosen random and uniform (won't have an effect if real_dataset is True)")
    parser.add_argument('--graph-type', type=int, default=0, help="if 0, a Holme-Kim graph is gonna be used, if 1 a Erdos-Riniy graph is gonna be used")
    parser.add_argument('--avarage-degree', type=int, default=10, help="avarage degree for every node")
    parser.add_argument('--p', type=int, default=0.4, help="probability of adding a triangle after adding edge (to be used ONLY with Holme-Kim)")
    parser.add_argument('--k', type=int, default=2, help="k as k-anonimity")
    parser.add_argument('--n', type=int, default=200, help="number of nodes in graph")
    parser.add_argument('--alpha', type=float, default=1, help="alpha + beta must equal 1")
    parser.add_argument('--repetitions', type=int, default=100, help="alpha + beta must equal 1")
    parser.add_argument('--seed', type=int, default=None, help="set seed to make experiments on the same dataset and graph")
    parser.add_argument('--csv', type=str, default="csv/query_results.csv", help="name of the file used to dump results")
    args = parser.parse_args()
    
    if args.graph_type == 0:
        G = graphgen.generate_powerlaw_graph(args.p, args.avarage_degree, args.n, from_dataset=args.real_dataset, seed=args.seed)
    elif args.graph_type == 1:
        G = graphgen.generate_ErdosRenyi_graph( args.n, args.avarage_degree, from_dataset=args.real_dataset, random_values=args.random_values, seed=args.seed)
    else:
        logging.error("graph type must be either 0 or 1")
        
    _, masked_G = anon.SaNGreeA(G, args.k, attributes_type, gen_trees, alpha=args.alpha, beta=1-args.alpha)
       
    repetitions = args.repetitions
    sum_percentages = 0
    min, max = get_dataset_possible_values()["age"]
    possible_values = list(range(min, max+1))
    if args.seed is not None:
        random.seed = args.seed
    for i in range(1, repetitions): 
        if possible_values == []:
            break
        random_num = random.choice(possible_values)
        possible_values.remove(random_num)
        true_finds = count_nodes_that_satisfy_query("age", random_num, G)
        total_finds = count_nodes_that_satisfy_query_masked("age",  random_num, masked_G)
        if total_finds != 0:
            percentage_wrong_finds = (total_finds - true_finds) / total_finds
        else: percentage_wrong_finds = 0
        sum_percentages += percentage_wrong_finds  
    avarage_error_rate = sum_percentages / repetitions
    
    with open(args.csv, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([args.n, args.alpha, avarage_error_rate])
    
    

if __name__ == '__main__':
    main()
