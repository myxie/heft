# Generates cost matrices based on given number of nodes and processors
import os
import networkx as nx

from heft.heft import Task
from graph import random_comp_matrix, random_comm_matrix

nodes = 1000;
processors = 16;

# generates comp matrices
# for x in range(0,nodes):
#   # for y in range(1,5000): 
#           # random_comp_matrix(x,y,50) 
#   random_comm_matrix(nodes,200,500)   


location = '/home/artichoke/Dropbox/thesis/data/input/graphml/'
graphs = [] 

for val in os.listdir(location):
    graphs.append(location+val)
count = 0 
for path in graphs:
    graph = nx.read_graphml(path,Task)
    num_nodes= len(graph.nodes())

    if num_nodes > 5000:
        continue
    random_comm_matrix(num_nodes,200,500)


# 771, 108,1202,135,3,19603,3467,1095,7719,12498,3271,29227,2899,1615,4583,2068