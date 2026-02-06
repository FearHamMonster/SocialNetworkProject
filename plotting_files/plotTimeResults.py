import csv
import matplotlib.pyplot as plt
import argparse
from collections import defaultdict
import numpy as np

def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--csv', type=str, default="csv/time_results.csv", help="the file to read results from")
    parser.add_argument('--title', type=str, default="Time Results", help="title of graph")
    parser.add_argument('--plot', type=bool, default=False, help="if false, show the plot, else, save it on disk")
    args = parser.parse_args()
    
    k_to_times = defaultdict(list)
    xvalues = []
    max_time = 0
    with open(args.csv, newline="") as f:
        reader = csv.reader(f)
        for k, n, time in reader:
            k = int(k)
            n = int(n)
            time = float(time)
                        
            if n not in xvalues:
                xvalues.append(n)
            
            k_to_times[k].append(time)
            if max_time < time:
                max_time = time
            
    for k in k_to_times.keys():
        plt.plot(xvalues, k_to_times[k], label="k =" + str(k))
    plt.xlabel("Number of nodes")
    plt.ylabel("Time(s)")
    plt.yticks(np.arange(0, 250, 25))
    plt.title(args.title)
    plt.legend()

    if(args.plot):
        plt.show()
    else:
        path = "plots/" + args.title + "_time.pdf"
        try:
            plt.savefig(path, dpi=300, bbox_inches="tight")
            print("Graph succesfully saved in path ", path, "!" )
        except Exception as e:
            print(f"Error in saving graph to disk {e}")

    

    
if __name__ == '__main__':
    main()