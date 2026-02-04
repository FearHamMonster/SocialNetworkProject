import csv
import matplotlib.pyplot as plt
import argparse
import numpy as np
from collections import defaultdict

def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--csv', type=str, default="csv/utility_results.csv", help="the file to read results from")
    parser.add_argument('--title', type=str, help="title of graph")
    parser.add_argument('--plot', type=bool, default=False, help="if false, show the plot, else, save it on disk")
    args = parser.parse_args()

    alpha_to_y = defaultdict(lambda: [[],[]])
    k_values = []
    with open(args.csv, newline="") as f:
        reader = csv.reader(f)
        for k, alpha, nsil, ngil in reader:
            k = int(k)
            alpha = float(alpha)
            nsil = float(nsil)
            ngil = float(ngil)
            if k not in k_values:
                k_values.append(k)
            alpha_to_y[alpha][0].append(nsil)
            alpha_to_y[alpha][1].append(ngil)
    width = 0.2
    k_pos = np.arange(len(k_values))  
    curr_shift = 0
    for alpha in alpha_to_y.keys():
        curr_label = "alpha=" + str(alpha) 
        plt.bar(k_pos + curr_shift, alpha_to_y[alpha][0], width=width, label=curr_label)
        curr_shift += width

    plt.title("NSIL " +args.title)
    plt.xticks(k_pos, k_values)   
    plt.xlabel("k")
    plt.ylabel("NSIL")
    plt.legend()

    if(args.plot):
        plt.show()
    else:
        path = "plots/nsil " + args.title + ".pdf"
        try:
            plt.savefig(path, dpi=300, bbox_inches="tight")
            print("Graph succesfully saved in path ", path, "!" )
        except Exception as e:
            print(f"Error in saving graph to disk {e}")
    plt.clf()
    
    curr_shift = 0
    for alpha in alpha_to_y.keys():
        curr_label = "alpha=" + str(alpha) 
        plt.bar(k_pos + curr_shift, alpha_to_y[alpha][1], width=width, label=curr_label)
        curr_shift += width

    plt.title("NGIL " + args.title)
    plt.xticks(k_pos, k_values)   
    plt.xlabel("k")
    plt.ylabel("NGIL")
    plt.legend()
    if(args.plot):
        plt.show()
    else:
        path = "plots/ngil " + args.title + ".pdf"
        try:
            plt.savefig(path, dpi=300, bbox_inches="tight")
            print("Graph succesfully saved in path ", path, "!" )
        except Exception as e:
            print(f"Error in saving graph to disk {e}")
    
        

    
if __name__ == '__main__':
    main()