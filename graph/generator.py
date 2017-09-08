# Generates cost matrices based on given number of nodes and processors

from graph import random_comp_matrix, random_comm_matrix

nodes = 1000;
processors = 16;

# generates comp matrices
for x in range(8,processors+1,4):
	for y in range(1,5000): 
			random_comp_matrix(x,y,50) 
# random_comm_matrix(30000,50)	

# 771, 108,1202,135,3,19603,3467,1095,7719,12498,3271,29227,2899,1615,4583,2068