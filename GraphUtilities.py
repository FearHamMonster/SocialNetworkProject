import networkx as nx
import matplotlib.pyplot as plt
import random 

def draw_with_labels(G):
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, font_weight='bold')
    node_labels = nx.get_node_attributes(G, 'label')  
    label_pos = {
        n: (x, y + 0.05)
        for n, (x, y) in pos.items()
    }
    nx.draw_networkx_labels(G, label_pos, labels=node_labels, font_size=16, font_weight='bold', verticalalignment='bottom')
    plt.show()    
    
def draw(G):
    nx.draw(G, with_labels=True, font_weight='bold')
    plt.show()
        
def draw_neighborhood(v, G):
    neighbors = G.subgraph(nx.neighbors(G, v)).copy()
    neighbors.add_node(v)
    neighbors = G.subgraph(neighbors)                 
    draw_with_labels(neighbors)


def get_nodes_names_by_degree(G):
    nodes = list(G.nodes)
    sorted(nodes, key=lambda v: G.degree[v], reverse=True)
    return nodes

def construct_random_graph(num_of_nodes, num_edges_to_remove =0 ):
    G = nx.complete_graph(num_of_nodes)
    if(num_edges_to_remove == 0 ):
        num_edges_to_remove = 3 * num_of_nodes
    counter = 0
    while(counter < num_edges_to_remove):
        edges = list(G.edges)
        edge = edges[random.randint(0, len(edges)-1)]
        if(G.degree[edge[0]] > 0 and G.degree[edge[1]]>0):
            G.remove_edge(edge[0],edge[1])
            counter += 1
    degrees = []
    for node in G.nodes:
        degrees.append(G.degree(node))
    degrees = sorted(degrees, reverse=True)
    return G, degrees        
        