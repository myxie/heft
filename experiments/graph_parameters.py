import os
import csv
import collections
import ast

import networkx as nx
import argparse

from heft.heft import Task, Heft



"""
Graph parameterisation script for DALiuGE Graphs
"""
test = '/home/artichoke/Dropbox/thesis/data/input/graphml/translated_test_seq_gather.graphml'

location = '/home/artichoke/Dropbox/thesis/data/input/graphml/'
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

def read_matrix(matrix):
    lines = [] 
    with open(matrix) as f:
        next(f)
        for line in f:
            line = ast.literal_eval(line)
            lines.append(line)
    return lines 


def graph_width_and_levels(path):
    graph = nx.read_graphml(path, Task)
    num = len(graph.nodes())
    levels = [0 for x in range(0,num)] 
    
    for node in graph.nodes():
        if list(graph.predecessors(node)) is None:
            levels[node.tid]=1
        else:
            pred = list(graph.predecessors(node))
            tmp = -1
            for task in pred:
                level = levels[task.tid]
                if level > tmp:
                    tmp = level
            levels[node.tid]=tmp+1
    
    print levels

    counter = collections.Counter(levels)
    width =max(counter.values())

    return levels[len(levels)-1],width

def fork_graph_levels(path):
    graph = nx.read_graphml(path, Task)
    num = len(graph.nodes())
    levels = [0 for x in range(0,num)] 
    
    for node in graph.nodes():
        if list(graph.predecessors(node)) is None:
            levels[node.tid]=1
        else:
            pred = list(graph.predecessors(node))
            tmp = -1
            for task in pred:
                level = levels[task.tid]
                if level > tmp:
                    tmp = level
            levels[node.tid]=tmp+1

    y = collections.Counter(levels)
    fork_levels = len([i for i in y if y[i]>1])
    # fork_levels = len(levels) - len(set(levels))


    return fork_levels

def graph_width(path):
    graph = nx.read_graphml(path,Task)
    width = 1
    for node in graph.nodes():
        if list(graph.predecessors(node)):
            if width < len(list(graph.predecessors(node))):
                width = len(list(graph.predecessors(node)))
        if list(graph.successors(node)):
            if width < len(list(graph.successors(node))):
                width = len(list(graph.predecessors(node)))

    return width


def num_params(num_processors,max_comp_num,max_comm_num):

    results = dict()

    for path in graphs: 
        graph = nx.read_graphml(path,Task)
        results[path]={'size':len(graph.nodes())}

    for path in graphs:
        graph = nx.read_graphml(path,Task)
        nodes = len(list(graph.nodes()))
        edges = len(list(graph.edges()))
        results[path]['edges']=edges

    for path in graphs:
        tmp_graph = nx.read_graphml(path,Task)
        if len(tmp_graph.nodes()) > 5000:
            results[path]['ccr'] = None
            continue
        results[path]['ccr'] = communcation_computation_cost(path,num_processors,max_comp_num,max_comm_num)


    for path in graphs:

        graph = nx.read_graphml(test,Task)
        size = len(graph.nodes())

        levels,width = graph_width_and_levels(path)
        parallel_level = max(levels-2,1)
        fork_level = max(fork_graph_levels(path),1)
        results[path]['levels'] = levels
       # results[path]['parallel_level']= parallel_level
        # results[path]['fork_graph_levels'] = fork_level

        # width = graph_width(path)
        results[path]['width']=width

        alpha_width = size/float(width)
        alpha_p_level = ((size)/(size-2))*parallel_level
        alpha_fj_level = ((size)/(size-fork_level))*fork_level

        p_alpha_width_diff = (abs(alpha_p_level - alpha_width))/float(alpha_width)
        p_alpha_parallel_diff = (abs(alpha_p_level - alpha_width))/float(alpha_p_level)

        parallel_val_final = 1 - min(p_alpha_width_diff,p_alpha_parallel_diff)


        fj_alpha_width_diff = (abs(alpha_fj_level - alpha_width))/float(alpha_width)
        fj_alpha_fj_diff = (abs(alpha_fj_level - alpha_width))/float(alpha_fj_level)
        
        fj_val_final = 1 - min(fj_alpha_width_diff,fj_alpha_fj_diff)

        results[path]['parallel'] = parallel_val_final
        results[path]['fork_join'] = fj_val_final

    count = 0
    file_headers='name'
    for res in results:
        if count is 0:
            for val in results[res]:
                file_headers = file_headers+','+str(val)
            file_headers=file_headers+'\n'

            with open('graph_parameters_comm-{0}_comp-{1}_{2}.csv'.format(max_comm_num, max_comp_num,num_processors),'w+') as f:
                f.write(file_headers)
            count = count+1
        line = "{0},".format(res)
        for val in results[res]:
            line = line + str(results[res][val])+','
        line = line +'\n'
        with open('graph_parameters_comm-{0}_comp-{1}_{2}.csv'.format(max_comm_num, max_comp_num,num_processors),'a') as f:
            f.write(line)

    return 0


def communcation_computation_cost(path,num_processors,max_comp_num,max_comm_num):
    """
    Sum of computation costs of each node * number of nodes/ Sum of communication costs*number of edges
    """
    graph = nx.read_graphml(path,Task)
    size = len(graph.nodes())
    edges = list(graph.edges())
    
    comp_matrix = read_matrix('/home/artichoke/Dropbox/thesis/data/input/matrices/comp_{0}/comp_{1}-{2}.txt'.format(max_comp_num,size,num_processors))
    comm_matrix = read_matrix('/home/artichoke/Dropbox/thesis/data/input/matrices/comm_{0}/comm_{1}.txt'.format(max_comm_num,size))

    comp_sum = 1000000
    comm_sum = 0


    for p in range(0,num_processors):
        tmp = 0
        for x in range(0,size):
            tmp = tmp + comp_matrix[x][p]
        comp_sum = min(tmp,comp_sum)

    for node in list(graph.nodes()):
        print node.tid
        for successor in list(graph.successors(node)):
            # print comm_sum
            comm_sum = comm_sum + comm_matrix[node.tid][successor.tid]

    denominator = comp_sum*size 
    numerator = comm_sum*len(edges)
    #print denominator
    ccr = numerator/float(denominator)
    print ccr 
    return ccr



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--processor", help="number of processors")
    parser.add_argument("--comm",help="maximum communication cost")
    parser.add_argument("--comp",help="maximum computation cost")
    args = parser.parse_args()
    num_processors = 2
    max_comm_num = 50 
    max_comp_num = 50  

    if args.processor:
        num_processors = int(args.processor)
        print("Number of processors: {0}".format(args.processor))
    if args.comm:
        max_comm_num = int(args.comm)
        print("Maximum communication cost: {0}".format(args.comm))
    if args.comp:
        max_comp_num = int(args.comp)
        print("Maximum computation cost: {0}".format(args.comp))
     
    num_params(num_processors,max_comp_num,max_comm_num)
    # results = dict()
    # graph_levels(test)


    # print results['ccr']
    # print  communcation_computation_cost(test)
    # graph = nx.read_graphml(test,Task)
    # size = len(graph.nodes())
    # width = graph_width(test)
    # parallel_levels = graph_levels(test)-2
    # fork_levels = fork_graph_levels(test)

    # print size
    # print width
    # alpha_width = size/width
    # alpha_p_level = ((size)/(size-2))*parallel_levels
    # alpha_fj_level = ((size)/(sizer-fork_levels))*fork_levels

    # print alpha_width
    # print alpha_p_level
    # print alpha_fj_level

    # print abs(alpha_fj_level - alpha_width)

    # print 1- (abs(alpha_p_level - alpha_width))/float(alpha_width)

    # print 1- (abs(alpha_fj_level - alpha_width))/float(alpha_width)




