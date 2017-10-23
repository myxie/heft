"""
Code to generate output for the CITS4008 Assignment 3

This will contain functions to do the following:

- Calculate rank for a pre-defined graph (not-random) for
example purposes within the body of the text
- Calculate the makespan of pre-defined graph
- Output information on the final schedule 

- Run the algorithm on random graphs with increased size,
and then plot the resulting makespan and time it takes to run 
the algorithm on a pyplot chart. 
"""
import os
import csv
import argparse
import networkx as nx
# import matplotlib.pyplot as plt

import numpy as np
import matplotlib.pyplot as plt
# from matplotlib import rc
# rc('font',**{'family':'serif','serif':['Computer Modern']})
# plt.style.use('ggplot')
# plt.style.use('bmh')



from heft.heft import Task, Heft
from graph.graph import random_task_dag,random_comp_matrix,random_comm_matrix 

"""
Requirements for new experiments:
    * Run through a folder of DALiuGE Graphs and read all the .graphml files
    * For each file
        - Convert it into a heft object
        - Calculate the rank based on a variety of ranking heuristics
        - For each of the different ranks, determine the final schedule based 
        on a variety of scheduling policies
        - Return this final schedule into some data format
"""

schedule_pairs_dict = {1:"Up + Greedy",2:"Up + Insertion", 3:"Up + OCT-Schedule", 4:"OCT + Greedy", 5:"OCT + Insertion", 6:"OCT + OCT Schedule"}
schedule_pairs_symbols = {1:'+',2:'x', 3:'D', 4:'s', 5:'^', 6:'*'}

def run_hefts(processor_num,location,matrices,max_comp_num,max_comm_num):
    heuristics = ['up','oct','random']
    # policies = ['insertion']
    policies   = ['insertion', 'oct_schedule', 'greedy']

    graphs = [] 
    # processor_num = 2
    max_comm_cost = max_comm_num
    max_comp_cost = max_comp_num
    for val in os.listdir(location):
       graphs.append(location+val)
    results = dict()
    for path in graphs:
        for heuristic in heuristics:
            for policy in policies:
                    print path
                    local_results = dict()
                    if os.path.exists(path): 
                        graph = nx.read_graphml(path,Task)
                        num_nodes= len(graph.nodes())
                        if num_nodes > 5000:
                            continue
                        comp_location=matrices+ 'comp_{0}/comp_{1}-{2}.txt'.format(max_comp_cost,num_nodes,processor_num)
                        comm_location = matrices + 'comm_{0}/comm_{1}.txt'.format(max_comm_cost,num_nodes)
                        heft = Heft(comp_location,comm_location,path)   
                        heft.rank(heuristic)
                        retval = heft.schedule(policy)
                        cp = heft.critical_path()
                        seq = heft.sequential_execution()
                        pair = str(heuristic) + ' ' + str(policy)

                        graph_name = path.split('/')[8] 
                        if graph_name in results:
                            results[graph_name][pair] = retval
                        else:
                            results[graph_name]={pair:retval,'size':num_nodes,'seq':seq,'cp':cp,}

    # results = run_hefts()
    count = 0
    file_headers = 'name'
    for res in results: 
        if count is 0:
            for val in results[res]:
                file_headers = file_headers +','+val
            file_headers = file_headers+"\n"
            with open('/home/croutons/Dropbox/results_comp_{0}_comm_{1}_{2}.csv'.format(max_comp_cost,max_comm_cost,processor_num),'w+') as f:
                f.write(file_headers)
            count = count+1
        line = "{0},".format(res)
        for val in results[res]:
            line = line + str(results[res][val])+','
        line = line + '\n'
        with open('/home/croutons/Dropbox/results_comp_{0}_comm_{1}_{2}.csv'.format(max_comp_cost,max_comm_cost,processor_num),'a') as f:
            f.write(line)


    return results


def better_occurences():
    #colum[1-7] is where our different schedulers are
    """
    For each colum:
        For each row:
            Count how many of the other schedules is this one better than for this row
            add it to a 'row' count
        then this is the final count for the column?
    """
    title=""
    matrix = []
    with open('/home/artichoke/Dropbox/thesis/data/results/schedule_data/16-10-2017_schedule_2-processors_comp50-comm50.csv', 'r') as csvfile:
        results = csv.reader(csvfile, delimiter=',')
        for row in results:
            title=row
            break
        # results.next()
        for x in range(0,9):
            for row in results:
                tmp = []
                for y in range(x+1,10):
                    tmp.append(row[y])
                matrix.append(tmp)
                # print "{0} has row {1}".format(row[0],val)
    final_matrix = [[0 for x in range(0,9)] for y in range(0,9)]

    for i in range(0,9):
        for j in range(i+1,9):
            count = 0
            num = 1
            for row in matrix:
                # print "{0},{1}".format(row[i],row[j])
                if int(row[i]) < int(row[j]):
                    count = count+1
                num = num+1

            final_matrix[i][j] = float(count)/float(num-1)
            final_matrix[j][i] = 1-(float(count)/float(num-1))


    print title
    with open("output.csv", "wb") as f:
        writer = csv.writer(f)
        writer.writerows(final_matrix)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--min_processor", help="number of processors")
    parser.add_argument("--max_processor",help="number of processors")
    parser.add_argument("--graph_location",help="location of graphs")
    parser.add_argument("--matrix_location",help="location of cost matrices")
    parser.add_argument("--comm",help="maximum communication cost")
    parser.add_argument("--comp",help="maximum computation cost")
    args = parser.parse_args()
    graph_location = '/home/artichoke/Dropbox/thesis/data/input/graphml/'
    min_processor = 2
    max_processor = 2
    max_comm_num = 50 
    max_comp_num = 50  

    if args.min_processor:
        min_processor = int(args.min_processor)
        print("Min number of processors: {0}".format(args.max_processor))
    if args.max_processor:
        num_processors = int(args.max_processor)
        print("Max number of processors: {0}".format(args.max_processor))

    if args.graph_location:
        graph_location = str(args.graph_location)
    if args.matrix_location:
        matrix_location= str(args.matrix_location)
    if args.comm:
        max_comm_num = int(args.comm)
        print("Maximum communication cost: {0}".format(args.comm))
    if args.comp:
        max_comp_num = int(args.comp)
        print("Maximum computation cost: {0}".format(args.comp))
    # make_plots() 
    # generate_slr()
    # generate_speedup()

    run_hefts(min_processor,graph_location,matrix_location,max_comp_num,max_comm_num)
    # better_occurences()

