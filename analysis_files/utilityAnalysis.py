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
    parser.add_argument('--avarage-degree', type=int, default=10, help="avarage degree for every node")
    parser.add_argument('--p', type=float, default=0.4, help="probability of adding a triangle after adding edge (to be used ONLY with Holme-Kim)")
    parser.add_argument('--k', type=int, default=2, help="k as k-anonimity")
    parser.add_argument('--n', type=int, default=100, help="number of nodes in graph")
    parser.add_argument('--alpha', type=float, default=0.5, help="alpha + beta must equal 1")
    parser.add_argument('--seed', type=int, default=None, help="set seed to make experiments on the same dataset and graph")
    parser.add_argument('--csv', type=str, default="csv/utility_results.csv", help="name of the file used to dump results")
    parser.add_argument('--print', type=bool, default=True, help="if true, the results get printed in standard output, else they get written in the csv file (WARNING: risk of overwriting)")
    args = parser.parse_args()
    
    if args.graph_type == 0:
        G = graphgen.generate_powerlaw_graph(args.p, args.avarage_degree, args.n, from_dataset=args.real_dataset, seed=args.seed)
    elif args.graph_type == 1:
        G = graphgen.generate_ErdosRenyi_graph(args.n, args.avarage_degree, from_dataset=args.real_dataset, random_values=args.random_values, seed=args.seed)
    else:
        raise ValueError("graph type must be either 0 or 1")
        
    if args.n <= 0  or args.alpha < 0 or args.avarage_degree < 0 or args.p < 0 or args.k <= 1:
        raise ValueError("values can't be negative and k must be >= 2")
        
        
    clusters, _ = anon.SaNGreeA(G, args.k, attributes_type, gen_trees, alpha=args.alpha, beta=1-args.alpha)
    nsil = anon.NSIL(G, clusters)
    ngil = anon.NGIL(G, clusters, attributes_type, gen_trees)
    
    if not args.print:
        with open(args.csv, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([args.k, args.alpha, nsil, ngil])  
    else:
        print("k = ", args.k, " alpha = ", args.alpha, " nsil = ", nsil, " ngil = ", ngil)
    
    

if __name__ == '__main__':
    main()
