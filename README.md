# SAnGreeA



## Requisites
- Python 3.12


## Description
SAnGreeA is a graph clusterization k-anonymization greedy algorithm, that executes in quadratic time.
Given a certain undirected graph, where each node has some multidimensional data, the algorithm groups
each node in a different cluster of size >= k (trying to preserve as much as possible the structural
composition of the graph, and minimize the generalization information loss of each node).

After each node is assigned to a cluster, each node's information in a certain cluster is generalized
accordingly, and the original edges that connected the nodes in the original graph are obscured.

The information that ends up being published in this masked graph, is:
 - The number of edges that connect nodes in a certain cluster (intra-cluster edges)
 - The number of edges that connect nodes from a cluster to nodes in another clusters (inter-cluster edges)
 - the number of nodes in a cluster (cluster size)

Each cluster in the final masked graph is represented as a node, which is labeled with the respective
cluster size and intra cluster edges, and clusters are connected by edges labaled with their inter-cluster 
number (of course, if this number is at least 1).

Sangreea.py executes this algorithm: to indicate the various parameters (like graph type, number of nodes...)
execute 
```python
    python -m Sangreea --help
```  
And each parameter and its meaning will be explained.

SaNGreeA takes two additional parameters, alpha and beta, which always add up to 1. Alpha is a constant
that regulates the generalization information loss (NGIL), whereas beta is a number that regulates the strucutral information loss (NSIL). It's sufficient to specify alpha, since beta is always 1-alpha.
The higher alpha is, the more NGIL is minimized 
The higher beta is, the more NSIL is minimized
It's automatically set as 0.5 as that represents the most balanced trade-off.

## Installation
```bash
git clone https://github.com/FearHamMonster/SocialNetworkProject.git
cd SocialNetworkProject

python -m venv venv
source venv/bin/activate   # Linux/macOS
# venv\Scripts\activate    # Windows

pip install -r requirements.txt  
```

# Usage
## Single Use Test
- Each of the files in analysis_files analyse different aspects of the algorithm
    - time_analysis: measures how much the algorithm takes to execute (calculated on an avarage)
    - utility_analysis: measures how much information was lost after the anonyimization of the dataset
    - horizontalTimeAnalysis: measures how much time the algorithms takes (number of QI attributes customizable)
    - queryAnalysis: measures the percentage of wrong queries on the anonymized dataset

Each of these files takes a list of parameters, they can be viewed with:
```bash 
python -m analysis_files.some_file_inside --help 
```
The --print parameter is automatically set on "True", and for the purpose of single use tests, it's important
to leave it True.

## Multiple Tests
To automatically execute tests in batch with predefined values, simply execute the batch files in batch/tests,
(they each will take several minutes unless parameters are manually changed inside)
These batch tests will automtically save the results as plots, saved in the plots directory.

The already existing plots in the plots folder are the results of executing each of the batch tests.

## Other Files
- The remaining files and their role:
    - anon.py: the library that includes every funcionality necessary for Sangreea to work
    - dataSetUtils.py: library used to infer the empirical distribution of the original dataset
    - downloadDataSet.py: file that downloads the dataset, can be called simply with "python -m downloadDataSet"
    - dataSetHierarchies.py: here each attribute is defined as either numerical or categorical, and the relative generalization tree for each attribute   
    - getQITrees.py: here is when all the trees for categorical attributes are manually defined
    - GraphUtilities.py: small library for viewing graphs
    - Node.py: the library used to implement the Tree data structure
    - Sangreea.py: the python file that executes Sangreea and outputs the masked graph

 

