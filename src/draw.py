"""
Graph drawing practise
"""

import matplotlib.pyplot as plt
import networkx as nx

def draw_graph(graph):
    G = graph 
    nx.draw(G, with_labels=True)
    plt.show()
