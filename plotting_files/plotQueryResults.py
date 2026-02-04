import csv
import matplotlib.pyplot as plt
import argparse
import numpy as np
from collections import defaultdict

def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--csv', type=str, default="csv/query_results.csv", help="the file to read results from")
    parser.add_argument('--title', type=str, default="", help="the title of the graph")
    parser.add_argument('--plot', type=bool, default=False, help="if false, show the plot, else, save it on disk")
    args = parser.parse_args()

    alpha_to_error = defaultdict(list)
    n_values = []
    with open(args.csv, newline="") as f:
        reader = csv.reader(f)
        for n, alpha, error_rate in reader:
            n = int(n)
            alpha = float(alpha)
            error_rate = float(error_rate)
            if n not in n_values:
                n_values.append(n)
            alpha_to_error[alpha].append(error_rate)

    width = 0.2
    x_pos = np.arange(len(n_values))  
    curr_shift = 0
    for alpha in alpha_to_error.keys():
        curr_label = "alpha=" + str(alpha) 
        plt.bar(x_pos + curr_shift, alpha_to_error[alpha], width=width, label=curr_label)
        curr_shift += width

    plt.title("Query Error Rate for " + args.title)
    plt.xticks(x_pos, n_values)   
    plt.xlabel("n")
    plt.ylabel("Error Rate")
    plt.legend()
    path = "plots/" + args.title + "query error rate.pdf"
    if(args.plot):
        plt.show()
    else:
        try:
            plt.savefig(path, dpi=300, bbox_inches="tight")
            print("Graph succesfully saved in path ", path, "!" )
        except Exception as e:
            print(f"Error in saving graph to disk {e}")
        plt.clf()
    
        

    
if __name__ == '__main__':
    main()