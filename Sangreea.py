import argparse
import generateGraph as graphgen
import csv
import logging
import anon
from dataSetHierarchies import attributes_type, gen_trees

def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--real-dataset', type=bool, default=True, help="a real dataset is gonna be used (if false, a synthetic one will be constructed with the same distribution as the first one)")
    parser.add_argument('--random-values', type=bool, default=False, help="values of attributes will be chosen random and uniform (won't have an effect if real_dataset is True)")
    parser.add_argument('--graph-type', type=int, default=0, help="if 0, a Holme-Kim graph is gonna be used, if 1 a Erdos-Riniy graph is gonna be used")
    parser.add_argument('--avarage-degree', type=int, default=3, help="avarage degree for every node")
    parser.add_argument('--p', type=float, default=0.4, help="probability of adding a triangle after adding edge (to be used ONLY with Holme-Kim)")
    parser.add_argument('--k', type=int, default=2, help="k as k-anonimity")
    parser.add_argument('--n', type=int, default=10, help="number of nodes in graph")
    parser.add_argument('--alpha', type=float, default=0.5, help="alpha + beta must equal 1")
    parser.add_argument('--seed', type=int, default=None, help="set seed to make experiments on the same dataset and graph")
    parser.add_argument('--show_graphs', type=bool, default=True, help="if True, original and masked graph are displayed")
    args = parser.parse_args()
    
    if args.graph_type == 0:
        G = graphgen.generate_powerlaw_graph(args.p, args.avarage_degree, args.n, from_dataset=args.real_dataset, seed=args.seed)
    elif args.graph_type == 1:
        G = graphgen.generate_ErdosRenyi_graph(args.n, args.avarage_degree, from_dataset=args.real_dataset, random_values=args.random_values, seed=args.seed)
    else:
        logging.error("graph type must be either 0 or 1")
        
    anon.SaNGreeA(G, args.k, attributes_type, gen_trees, alpha=args.alpha, beta=1-args.alpha, show_graphs=args.show_graphs)
    
    

if __name__ == '__main__':
    main()
