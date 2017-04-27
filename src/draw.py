"""
Graph drawing practise
"""

import matplotlib.pyplot as plt
import networkx as nx

def draw_graph(graph):
    G = nx.gn_graph(10)  
    nx.draw(G, with_labels=True)
    plt.show()
