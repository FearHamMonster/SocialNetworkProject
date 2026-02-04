import csv
import matplotlib.pyplot as plt
import argparse
from collections import defaultdict

def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--csv', type=str, default="csv/horizontal_time_results.csv",help="the file to read results from")
    parser.add_argument('--title', type=str, default="Horizontal Time Results", help="title of graph")
    parser.add_argument('--plot', type=bool, default=False, help="if false, show the plot, else, save it on disk")
    args = parser.parse_args()
    
    xvalues = []
    yvalues = []
    with open(args.csv, newline="") as f:
        reader = csv.reader(f)
        for num_of_attr, time in reader:
            xvalues.append(int(num_of_attr))
            yvalues.append(float(time))

    plt.plot(xvalues, yvalues)

    plt.xlabel("Number of QI attributes")
    plt.ylabel("Time(s)")
    plt.title(args.title)
    path = "plots/" + args.title + ".pdf"
    if(args.plot):
        plt.show()
    else:
        try:
            plt.savefig(path, dpi=300, bbox_inches="tight")
            print("Graph succesfully saved in path ", path, "!" )
        except Exception as e:
            print(f"Error in saving graph to disk {e}")

    

    
if __name__ == '__main__':
    main()