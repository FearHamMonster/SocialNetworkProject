import networkx as nx
import numpy as np
import getQITrees as trees
import matplotlib.pyplot as plt 
import math
import GraphUtilities as utils

#GENERALIZATION LOSS FUNCTIONS__________________

#Generalization Information for whole graph
#returns a dictionary that maps attribute to generalization
def GI_global(G, attributes_type, gen_trees):
   generalizations = {}
   nodes_record = nx.get_node_attributes(G, "QIs")
   for attribute in attributes_type.keys():
        if attributes_type[attribute] == "numerical":
            min = np.inf
            max = 0
            for node in G.nodes:
                cluster_node_attr = int(nodes_record[node][attribute]) 
                if min > cluster_node_attr:
                    min = cluster_node_attr
                if max < cluster_node_attr:
                    max = cluster_node_attr
            generalizations[attribute] = (min, max)
        else: #categorical
            generalizations[attribute] = gen_trees[attribute]  
   return generalizations
              
    

#Generalization Information for certain Cluster
#returns a dictionary that maps the cluster attributes to their generalization
def GI(G, cluster, attributes_type, gen_trees):
    generalizations = {}
    nodes_record = nx.get_node_attributes(G, "QIs")
    for attribute in attributes_type.keys():
        if attributes_type[attribute] == "numerical":
            min = np.inf
            max = 0
            for cluster_node in cluster:
                cluster_node_attr = int(nodes_record[cluster_node][attribute]) 
                if min > cluster_node_attr:
                    min = cluster_node_attr
                if max < cluster_node_attr:
                    max = cluster_node_attr
            generalizations[attribute] = (min, max)
                
        else: #categorical
            if len(cluster) < 2:
                lca_label = nodes_record[cluster[0]][attribute]
            else:
                lca_label =  gen_trees[attribute].lowest_common_ancestor(nodes_record[cluster[0]][attribute], nodes_record[cluster[1]][attribute]) 
                for i in range(2, len(cluster)):
                    cluster_node_attr = nodes_record[cluster[i]][attribute] 
                    lca_label = gen_trees[attribute].lowest_common_ancestor(lca_label, cluster_node_attr)
            generalizations[attribute] = lca_label
    return generalizations
            
def size(interval):
    return interval[1] - interval[0]


# Generalization Information Loss for cluster
def GIL(G, cluster, attributes_type, gen_trees, graph_dict):
    current_first_term_sum = 0 
    current_second_term_sum = 0 
    cluster_dict = GI(G, cluster, attributes_type, gen_trees)
    for attribute in attributes_type.keys():
        if attributes_type[attribute] == "numerical":
            first_term = size(cluster_dict[attribute])
            first_term /= size(graph_dict[attribute])
            current_first_term_sum += first_term

        if attributes_type[attribute] == "categorical":
            second_term = gen_trees[attribute].height_of_label(cluster_dict[attribute]) / graph_dict[attribute].height()
            current_second_term_sum += second_term
    return len(cluster) * (current_first_term_sum + current_second_term_sum)

# Total Generalization Information Loss for every cluster
def Total_GIL(G, clusters, attributes_type, gen_trees, graph_dict):
    counter = 0
    for cluster in clusters:
        cost = GIL(G, cluster, attributes_type, gen_trees, graph_dict) 
        counter += cost
    return counter

# Normalized Total Generalization Information Loss for every cluster
def NGIL(G, clusters, attributes_type, gen_trees, graph_dict=None):
    if graph_dict is None:
        graph_dict = GI_global(G, attributes_type, gen_trees)
    numerator = Total_GIL(G, clusters, attributes_type, gen_trees, graph_dict) 
    denominator = nodes_in_clusters(clusters) * len(attributes_type)
    ngil = numerator / denominator
    assert 0 <= ngil <= 1
    return ngil

def nodes_in_clusters(clusters):
    count = 0
    for cluster in clusters:
        count += len(cluster)
    return count

#STRUCTURAL LOSS FUNCTIONS________________________
def intraSIL(cluster, G):  
    cluster_subgraph = G.subgraph(cluster)
    cluster_edges = cluster_subgraph.number_of_edges()
    return 2 * cluster_edges * (1 - cluster_edges / math.comb(len(cluster), 2))
    

def interSIL(cluster1, cluster2, G):
    edges_between_clusters = count_edges_in_clusters(cluster1, cluster2, G)
    return 2 * edges_between_clusters * ( 1 - edges_between_clusters / (len(cluster1) * len(cluster2)) )

#Total Structural Information Loss for every cluster 
def SIL(G, clusters):
    intraSil_sum = 0
    for cluster in clusters:
        intraSil_sum += intraSIL(cluster, G)
    
    interSil_sum = 0
    for i in range(len(clusters)-1):
        for j in range(i+1, len(clusters)):
            interSil_sum += interSIL(clusters[i], clusters[j], G)
    return intraSil_sum + interSil_sum

#Normalized Total Structural Information Loss for every cluster 
def NSIL(G, clusters):
    n = G.number_of_nodes()
    nsil = SIL(G, clusters) / (n * (n-1) / 4) 
    assert 0 <= nsil <=1
    return nsil

def dist_nodes(node1, node2, G):
    dist = 0
    for neighbor in G.neighbors(node1):
        if not G.has_edge(neighbor, node2) and neighbor != node2:
            dist += 1
    for neighbor in G.neighbors(node2):
        if not G.has_edge(neighbor, node1) and neighbor != node1:
            dist += 1
    return dist / (G.number_of_nodes() - 2)

def dist_node_cluster(node, cluster, G):
    counter = 0
    for cluster_node in cluster:
        counter += dist_nodes(node, cluster_node, G)
    distance = counter / len(cluster)
    assert 0 <= distance <= 1
    return distance 

#FINAL ALGORITHM____________________

def clustering_cost(node, cluster, G, attributes_type, gen_trees, graph_dict, alpha, beta):
    cost = alpha *  NGIL(G, [cluster + [node]], attributes_type, gen_trees, graph_dict)  + beta * dist_node_cluster(node, cluster, G)
    assert 0 <= cost <= 1
    return cost

def find_min_cost_vertex(G, unclustered_nodes, cluster, attributes_type, gen_trees, graph_dict, alpha, beta):
    nodes = unclustered_nodes
    min_node = nodes[0]
    min_clustering_cost = clustering_cost(min_node, cluster, G, attributes_type, gen_trees, graph_dict, alpha, beta)
    for node in nodes:
        current_clustering_cost = clustering_cost(node, cluster, G, attributes_type, gen_trees, graph_dict, alpha, beta)  
        if(current_clustering_cost < min_clustering_cost):
            min_node = node
            min_clustering_cost = current_clustering_cost
    return min_node

def SaNGreeA(G, k, attributes_type, gen_trees, alpha=0.5, beta=0.5, show_graphs = False):
    G = G.copy()
    if show_graphs:
        show_original_network(G) 
    graph_dict = GI_global(G, attributes_type, gen_trees)
    clusters = []
    unclustered_nodes = list(G.nodes)
    while unclustered_nodes != []:
        max_degree_node = max(unclustered_nodes, key=lambda v: G.degree(v))
        cluster = [max_degree_node]
        unclustered_nodes.remove(max_degree_node)
        while(len(cluster) < k and unclustered_nodes != []):
            min_node = find_min_cost_vertex(G, unclustered_nodes, cluster, attributes_type, gen_trees, graph_dict, alpha, beta)
            cluster.append(min_node)
            unclustered_nodes.remove(min_node)            
        if (len(cluster) < k):
            DisperseCluster(cluster, clusters, G, attributes_type, gen_trees, graph_dict, alpha, beta)
        else:
            clusters.append(cluster)  
    masked_G = create_masked_network(clusters, G, attributes_type, gen_trees)
    if show_graphs:
        print(clusters)
        show_masked_network(masked_G)
    
    if not checkKanonimity(clusters, k):
        print("K anonimity not reached")
    return clusters, masked_G

def create_masked_network(clusters, G, attributes_type, gen_trees):
    masked_G = nx.Graph()
    for i in range(len(clusters)):
        generalization = GI(G, clusters[i], attributes_type, gen_trees)
        masked_G.add_node(i, QIs=generalization, intra_gen=intra_cluster_gen(clusters[i], G))
    
    for i in range(len(clusters)-1):
        for j in range(i+1, len(clusters)):
            inter_edges = count_edges_in_clusters(clusters[i], clusters[j], G)
            if inter_edges > 0:
                masked_G.add_edge(i, j, inter_gen=inter_edges)
    return masked_G
                
    
def show_masked_network(masked_G):
    print("MASKED GRAPH NODES WITH GENERALIZATIONS")
    for node in masked_G.nodes:
        print(node, masked_G.nodes[node]["QIs"], masked_G.nodes[node]["intra_gen"])
    pos = nx.spring_layout(masked_G)
    nx.draw(masked_G, pos, with_labels=True)
    edge_labels = nx.get_edge_attributes(masked_G, "inter_gen")
    nx.draw_networkx_edge_labels(masked_G, pos, edge_labels=edge_labels)
    plt.show()

def show_original_network(G):
    print("ORIGINAL GRAPH NODES WITH VALUES")
    for node in G.nodes:
        print(node, G.nodes[node]["QIs"])
    utils.draw(G)
    

def intra_cluster_gen(cluster, G):
    cluster_subgraph = G.subgraph(cluster)
    cluster_edges = cluster_subgraph.number_of_edges()
    cluster_cardinality = len(cluster)
    return (cluster_cardinality, cluster_edges)        
        
def count_edges_in_clusters(cluster1, cluster2, G):
    counter = 0
    for node1 in cluster1:
        for node2 in cluster2:
            if G.has_edge(node1, node2):
                counter += 1
    return counter 

            
def DisperseCluster(cluster, clusters, G, attributes_type, gen_trees, graph_dict, alpha, beta):
    for cluster_node in cluster:
        best_cluster = FindBestCluster(cluster_node, clusters, G, attributes_type, gen_trees, graph_dict, alpha, beta)
        best_cluster.append(cluster_node)
    
    
def FindBestCluster(node, clusters, G, attributes_type, gen_trees, graph_dict, alpha, beta):
    min_clustering_cost = clustering_cost(node, clusters[0], G, attributes_type, gen_trees, graph_dict, alpha, beta)
    best_cluster = clusters[0]
    for current_cluster in clusters:
        current_clustering_cost = clustering_cost(node, current_cluster, G, attributes_type, gen_trees, graph_dict, alpha, beta)
        if(current_clustering_cost < min_clustering_cost):
            best_cluster = current_cluster
            min_clustering_cost = current_clustering_cost
    return best_cluster

def checkKanonimity(clusters, k):
    for cluster in clusters:
        if len(cluster) < k:
            return False
    return True
                