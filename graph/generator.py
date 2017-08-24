# Generates cost matrices based on given number of nodes and processors

from graph import random_comp_matrix, random_comm_matrix

nodes = 1000;
processors = 5;

# generates comp matrices
# for x in range(1,processors+1):
for y in range(131,150): 
    # random_comp_matrix(x, y, 15) 
    random_comm_matrix(y,50)
