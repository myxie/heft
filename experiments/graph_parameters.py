import os
import csv

import networkx as nx
# import matplotlib.pyplot as plt

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
rc('font',**{'family':'serif','serif':['Computer Modern']})

from heft.heft import Task, Heft

"""
Graph parameterisation script for DALiuGE Graphs
"""


location = '/home/hummus/Dropbox/thesis/data/input/graphml/'
graphs = [] 

for val in os.listdir(location):
   graphs.append(location+val)

"""
Graphs have the following parameters:

Size
Levels
Branching factor
Fork-join alpha error
Parallel alpha error
Sequential branching 
"""

def num_params():

    results = dict()

    for path in graphs: 
        graph = nx.read_graphml(path,Task)
        results[path]={'size':len(graph.nodes())}

    for path in graphs:
        graph = nx.read_graphml(path,Task)
        nodes = len(graph.nodes())
        edges = len(graph.edges())
        results[path]['BF']=float(edges)/float(nodes)

    count = 0
    file_headers='name'
    for res in results:
        if count is 0:
            for val in results[res]:
                file_headers = file_headers+','+val
            file_headers=file_headers+'\n'

            with open('graph_parameters.csv','w+') as f:
                f.write(file_headers)
            count = count+1
        line = "{0},".format(res)
        for val in results[res]:
            line = line + str(results[res][val])+','
        line = line +'\n'
        with open('graph_parameters.csv','a') as f:
            f.write(line)


def graph_levels(path):
    graph = nx.read_graphml(path, Task)
    num = len(graph.nodes())
    levels = [0 for x in range(0,num)] 
    
    for node in graph.nodes():
        if graph.predecessors(node) is None:
            levels[node.tid]=1
        else:
            pred = graph.predecessors(node)
            tmp = -1
            for task in pred:
                level = levels[task.tid]
                if level > tmp:
                    tmp = level
            levels[node.tid]=tmp+1

    return levels


if __name__ == '__main__':
    print graph_levels('/home/hummus/Dropbox/thesis/data/input/graphml/translated_chiles_simple.graphml')
