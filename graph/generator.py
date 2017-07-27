# Generates cost matrices based on given number of nodes and processors

from graph import random_comp_matrix, random_comm_matrix

nodes = 150;
processors = 5;

# generates comp matrices
#for x in range(1,processors+1):
for y in range(100,150): 
    random_comp_matrix(3, y, 15) 

random_comm_matrix(130,50)
