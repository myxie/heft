# Generates cost matrices based on given number of nodes and processors

from graph import random_comp_matrix, random_comm_matrix

nodes = 10;
processors = 5;

# generates comp matrices
for x in range(1,processors+1):
   random_comp_matrix(x, nodes, 15) 

random_comm_matrix(nodes,50)
