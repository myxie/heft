# Generates cost matrices based on given number of nodes and processors
import os
import networkx as nx
import argparse

from heft.heft import Task
from graph import random_comp_matrix, random_comm_matrix

# nodes = 1000;
# processors = 16;

# generates comp matrices
# for x in range(0,nodes):
#   # for y in range(1,5000): 
#           # random_comp_matrix(x,y,50) 
#   random_comm_matrix(nodes,200,500)   


location = '/home/artichoke/Dropbox/thesis/data/input/graphml/'
graphs = [] 
def generate_cost_matrix(comp_cost_min,comp_cost_max,comm_cost_min,comm_cost_max):
    for val in os.listdir(location):
        graphs.append(location+val)

    for path in graphs:
        print path
        graph = nx.read_graphml(path,Task)
        num_nodes= len(graph.nodes())

        if num_nodes > 5000:
            continue
        print path
        for x in range(2,9):
            random_comp_matrix(x,num_nodes,comp_cost_min,comp_cost_max)
            random_comm_matrix(num_nodes,comm_cost_min,comm_cost_max) 


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--processor", help="number of processors")
    parser.add_argument("--min_comp",help="maximum communication cost")
    parser.add_argument("--max_comp",help="maximum computation cost")
    parser.add_argument("--min_comm",help="maximum communication cost")
    parser.add_argument("--max_comm",help="maximum computation cost")

    args = parser.parse_args()
    num_processors = 2
    min_comm = 0
    max_comm = 50
    
    min_comp=0
    max_comp = 50 


    if args.min_comp:
        min_comp = int(args.min_comp)
        print("Minimum communication cost: {0}".format(args.min_comp))

    if args.max_comp:
        max_comp= int(args.max_comp)
        print("Maximum communication cost: {0}".format(args.max_comp))

    if args.min_comm:   
        min_comm = int(args.max_comm)
        print("Maximum computation cost: {0}".format(args.max_comm))    
    
    if args.max_comm:
        max_comm = int(args.max_comm)
        print("Maximum communication cost: {0}".format(args.max_comm))
    
    generate_cost_matrix(min_comp,max_comp, min_comm,max_comm)
    # num_params(num_processors,max_comm_num,max_comp_num)


# 771, 108,1202,135,3,19603,3467,1095,7719,12498,3271,29227,2899,1615,4583,2068