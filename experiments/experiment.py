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

import networkx as nx
# import matplotlib.pyplot as plt

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
rc('font',**{'family':'serif','serif':['Computer Modern']})
# plt.style.use('ggplot')
plt.style.use('bmh')



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

def run_hefts():
    heuristics = ['up', 'oct']
    policies   = ['insertion', 'oct_schedule', 'greedy']

    location = '/home/croutons/Dropbox/thesis/data/input/graphml/'
    graphs = [] 

    for val in os.listdir(location):
       graphs.append(location+val)
    results = dict()
    for path in graphs:
        for heuristic in heuristics:
            for policy in policies:
                local_results = dict()
                if os.path.exists(path): 
                    graph = nx.read_graphml(path,Task)
                    num= len(graph.nodes())
                    if num > 5000:
                        continue
                    heft = Heft('/home/croutons/Dropbox/thesis/data/input/matrices/comp/comp_{0}-3.txt'.format(num),\
                    '/home/croutons/Dropbox/thesis/data/input/matrices/comm/comm_{0}.txt'.format(num),path)   
                    heft.rank(heuristic)
                    retval = heft.schedule(policy)
                    cp = heft.critical_path()
                    seq = heft.sequential_execution()
                    pair = str(heuristic) + ' ' + str(policy)

                    if path in results:
                        results[path][pair] = retval
                    else:
                        results[path]={'size':num,'seq':seq,'cp':cp,pair:retval}

    # results = run_hefts()
    count = 0
    file_headers = 'name'
    for res in results: 
        if count is 0:
            for val in results[res]:
                file_headers = file_headers +','+val
            file_headers = file_headers+"\n"
            with open('results.csv','w+') as f:
                f.write(file_headers)
            count = count+1
        line = "{0},".format(res)
        for val in results[res]:
            line = line + str(results[res][val])+','
        line = line + '\n'
        with open('results.csv','a') as f:
            f.write(line)


    return results

def make_plots():

    # x_list = [x for x in range(0,1200)]

    with open('results.csv', 'r') as csvfile:
        results = csv.reader(csvfile, delimiter=',')
        results.next()

        plotter_y=dict()
        # plotter_y=dict()
        for row in results:
            for x in range(1,7):
                if x in plotter_y:
                    plotter_y[x].append((int(row[8]),row[x]))
                else:
                    plotter_y[x] = [(int(row[8]),row[x])]

            sorted(plotter_y[x],key=lambda x: x[0])
                # if x in plotter_x:
                #     plotter_x[x].append(row[8]) # this is the size of the graph
                # else:
                #     plotter_x[x] = [row[8]]

        # map(list, zip(*[(1, 2), (3, 4), (5, 6)]))
        map(list, zip(*(sorted(plotter_y[x],key=lambda x: x[0]))))

    for x in range(1,7):
        plt.rc('text', usetex=True)
        plt.rc('font', family='serif')
        plotvals = map(list, zip(*(sorted(plotter_y[x],key=lambda x: x[0]))))
        plt.plot(plotvals[0], plotvals[1],'-+', label = schedule_pairs_dict[x],linewidth=0.5 )
    
    plt.xlabel('Nodes')
    plt.ylabel('Schedule Makespan')

    plt.legend()
    plt.show()


def generate_slr():

    """
    This function gets the values output by the 'results' section and calculates performance metrics, include: 
    Schedule-to-Length ratio (SLR)
    Speedup
    Number of occurences of a better quality schedule
    Algorithmic running time
    """


    """
    SLR:  makespan/min_CP 
    
    We need to get each makespan and 'cp' value from the results.csv file and calculate the resultant slr 
    """

    with open('results.csv', 'r') as csvfile:
        results = csv.reader(csvfile, delimiter=',')
        results.next()

        plotter_y=dict()
        # plotter_y=dict()
        for row in results:
            for x in range(1,7):
                if x in plotter_y:
                    plotter_y[x].append((int(row[8]),(float(row[x])/float(row[7]))))
                else:
                    plotter_y[x] = [(int(row[8]),(float(row[x])/float(row[7])))]

            sorted(plotter_y[x],key=lambda x: x[0])
                # if x in plotter_x:
                #     plotter_x[x].append(row[8]) # this is the size of the graph
                # else:
                #     plotter_x[x] = [row[8]]

        # map(list, zip(*[(1, 2), (3, 4), (5, 6)]))
        map(list, zip(*(sorted(plotter_y[x],key=lambda x: x[0]))))

    for x in range(1,7):
        plt.rc('text', usetex=True)
        plt.rc('font', family='serif')
        plotvals = map(list, zip(*(sorted(plotter_y[x],key=lambda x: x[0]))))
        plt.plot(plotvals[0], plotvals[1],'-x', label = schedule_pairs_dict[x],linewidth=0.5 )

    plt.xlabel('Nodes')     
    plt.ylabel('SLR')
    plt.legend()
    plt.show()

def generate_speedup():

    """
    This function gets the values output by the 'results' section and calculates performance metrics, include: 
    Schedule-to-Length ratio (SLR)
    Speedup
    Number of occurences of a better quality schedule
    Algorithmic running time
    """

    """
    SLR:  sequential 
    
    We need to get each makespan and 'cp' value from the results.csv file and calculate the resultant slr 
    """

    with open('results.csv', 'r') as csvfile:
        results = csv.reader(csvfile, delimiter=',')
        results.next()

        plotter_y=dict()
        # plotter_y=dict()
        for row in results:
            for x in range(1,7):
                if x in plotter_y:
                    plotter_y[x].append((int(row[8]),(float(row[9])/float(row[x]))))
                else:
                    plotter_y[x] = [(int(row[8]),(float(row[9])/float(row[x])))]

            sorted(plotter_y[x],key=lambda x: x[0])
                # if x in plotter_x:
                #     plotter_x[x].append(row[8]) # this is the size of the graph
                # else:
                #     plotter_x[x] = [row[8]]

        # map(list, zip(*[(1, 2), (3, 4), (5, 6)]))
        map(list, zip(*(sorted(plotter_y[x],key=lambda x: x[0]))))

    for x in range(1,7):
        plt.rc('text', usetex=True)
        plt.rc('font', family='serif')
        plotvals = map(list, zip(*(sorted(plotter_y[x],key=lambda x: x[0]))))
        plt.plot(plotvals[0], plotvals[1],'-x', label = schedule_pairs_dict[x],linewidth=0.5 )

    plt.xlabel('Nodes')     
    plt.ylabel('Speedup')
    plt.legend()
    plt.show()


def better_occurences():
    #colum[1-7] is where our different schedulers are
    """
    For each colum:
        For each row:
            Count how many of the other schedules is this one better than for this row
            add it to a 'row' count
        then this is the final count for the column?
    """
    matrix = []
    with open('results.csv', 'r') as csvfile:
        results = csv.reader(csvfile, delimiter=',')
        results.next()
        for x in range(1):
            for row in results:
                tmp = []
                for y in range(x+1,8):
                    tmp.append(row[y])
                matrix.append(tmp)
                # print "{0} has row {1}".format(row[0],val)

    # better = dict()
    # for i in range(0,7):
    #     for j in range(i+1,7):
    #         count = 0
    #         num = 1
    #         for row in matrix:
    #             if row[i] < row[j]:
    #                 count = count +1 
    #             num = num+1 
    #         better[(i,j)] = float(count)/float(num-1)

    final_matrix = [[0 for x in range(0,6)] for y in range(0,6)]

    for i in range(0,6):
        for j in range(i+1,6):
            count = 0
            num = 1
            for row in matrix:
                # print "{0},{1}".format(row[i],row[j])
                if int(row[i]) < int(row[j]):
                    count = count+1
                num = num+1

            final_matrix[i][j] = float(count)/float(num-1)
            final_matrix[j][i] = 1-(float(count)/float(num-1))


    # for line in better:
    #     print "{0}: {1}".format(line, better[line])

    for row in final_matrix:
        print row

    # ?final_matrix = [x for x in [0 for y in range(0,7)]]

if __name__ == '__main__':
    make_plots()
    generate_slr()
    generate_speedup()
    # run_hefts()
    # better_occurences()
    




# # Deprecated and archaic setup
# def setup_graph():

#     """
#     We need: 
#     Graph
#     Computation matrix
#     communication matrix
#     Heft object 
#     """

#     graph = nx.DiGraph()
#     a,b,c,d,e,f =  Task(0),Task(1),Task(2),Task(3),Task(4),Task(5)
#     graph.add_nodes_from([a,b,c,d,e,f])
#     graph.add_edges_from([(a,b ),(a,c),(b,e),(c,d),(d,e),(e,f)])

#     comp_matrix={0:[7,5],1:[8,9],2:[4,15],3:[2,1],4:[8,5],5:[12,11]}

#     comm_matrix=[[0,7,12,0,0,0],[7,0,0,0,5,0],[12,0,0,6,0,0],\
#         [0,0,0,0,11,0],[0,5,0,11,0,9],[0,0,0,0,9,0]]

#     processors = create_processors(2)

#     heft = Heft(graph,comm_matrix,comp_matrix,2)
#     heft.rank_up(graph.nodes()[0])
#     #print    heft.top_sort_tasks()
#     for task in  heft.rank_sort_tasks():
#         print 'taskid: ' + str(task.tid) + ': '+ str(task.rank)
#     makespan_tuple = heft.insertion_policy()
#     for x in range(len(makespan_tuple[1])):
#         print makespan_tuple[1][x]

# # Deprecated and archaic testing functionality
# def dep_run_random_heft():
#     """
#     This runs the HEFT algorithm on an increasing number of nodes 
#     and adds each makespan onto a list 
#     """
#     nodes_init=10
#     nodes_final=1001
#     makespan_list = [] 
#     makespan_time_list = []
#     makespan_rank_time = []
#     makespan_insertion_time = []
#     top_make_list = []
#     top_time_list = []
#     # difference_list = []
#     num_processor = 2
#     #,2,3,4,5,3,4,5
#     n_list = [x for x in range(nodes_init,nodes_final,50)]
#     for x in [(4/float(3)),2,3,4,5]:   
#         for n in range(nodes_init, nodes_final, 50):
#             g = random_task_dag(n,float(x*n))
#             # p = create_processors(num_processor)
#             comp = random_comp_matrix(num_processor,n,20)
#             comm = random_comm_matrix(n,10)
#             heft = Heft(g,comm,comp,num_processor)
#             makespan_tuple = heft.makespan()
#             makespan_list.append(makespan_tuple[0])
#             makespan_time_list.append(makespan_tuple[1])
#             # makespan_rank_time.append(makespan_tuple[2])
#             # makespan_insertion_time.append(makespan_tuple[3])
#             topmakespan_tuple = heft.top_makespan()
#             top_make_list.append(topmakespan_tuple[0])
#             top_time_list.append(topmakespan_tuple[1])
        
#         # plt.plot(n_list, makespan_list,label=str(1/(float(x))))
#         # print zip(top_make_list,makespan_list)
#         # print [i-j for i,j in zip(top_make_list,makespan_list)]
#         # difference_list = [i - j for i, j in zip(top_make_list, makespan_list)]
#         output_file = open('output.txt','a')
#         output_file.write(str(makespan_time_list)+'\n')
#         output_file.write(str(top_time_list)+'\n')
#         output_file.write('******************************************************\n')
#         output_file.close()
#         plt.plot(n_list, makespan_time_list,label='Makespan: ' +str(1/float(x)))
#         plt.plot(n_list, top_time_list , label= 'Top: ' + str(1/float(x)))

#         #plt.plot(n_list,makespan_time_list,label='Total')
#         # plt.plot(n_list,makespan_rank_time,label='Rank')
#         # plt.plot(n_list,makespan_insertion_time,label='Insertion')
#         # plt.plot(n_list,top_time_list,label='Top')
#         makespan_list = [] 
#         makespan_time_list = []
#         top_make_list = []
#         top_time_list = []

#     plt.legend()
#     plt.show()

#     return makespan_list,makespan_time_list,top_make_list,top_time_list

# #TODO Change this to produce a nicer output
# def rank_heft():
#     nodes_init=10
#     nodes_final=1000
#     makespan_list = [] 
#     makespan_time_list = []
#     makespan_rank_time = []
#     makespan_insertion_time = []
#     top_make_list = []
#     top_time_list = []
#     max_make_list = []
#     min_make_list = []
#     # difference_list = []
#     num_processor = 2
#     #,2,3,4,5,3,4,5
#     max_count = 0
#     min_count =0
#     top_count = 0
#     n_list = [x for x in range(nodes_init,nodes_final,50)]
#     # for x in [(4/float(3)),2,3,4,5]:   
#     for n in range(nodes_init, nodes_final, 50):
#         g = random_task_dag(n,float(2*n))
#         p = create_processors(num_processor)
#         comp = random_comp_matrix(num_processor,n,20)
#         comm = random_comm_matrix(n,10)
#         heft = Heft(g,comm,comp,num_processor)
#         # top_heft = Heft(g,comm,comp,num_processor)

#         makespan_tuple = heft.makespan()
#         makespan_list.append(makespan_tuple[0])
#         # makespan_time_list.append(makespan_tuple[1])
#         # # makespan_rank_time.append(makespan_tuple[2])
#         # # makespan_insertion_time.append(makespan_tuple[3])
#         topmakespan_tuple = heft.top_makespan()
#         top_make_list.append(topmakespan_tuple[0])
#         # # top_time_list.append(topmakespan_tuple[1])
        
#         maxmakespan_tuple = heft.max_makespan()
#         max_make_list.append(maxmakespan_tuple[0])
#         minmakespan_tuple = heft.min_makespan()
#         min_make_list.append(minmakespan_tuple[0])

#         if (makespan_tuple[0] < maxmakespan_tuple[0]):
#             max_count = max_count + 1
#         if (makespan_tuple[0] < minmakespan_tuple[0]):
#             min_count = min_count + 1
#         if (makespan_tuple[0] < topmakespan_tuple[0]):
#             top_count = top_count + 1

#     plt.plot(n_list, makespan_list,label='Rank Sort')
#     plt.plot(n_list, top_make_list,label='Rank Sort')

#     output_file = open('output.txt','a')
#     output_file.write(str(makespan_list)+'\n')
#     output_file.write(str(top_make_list)+'\n')
#     output_file.write(str(max_make_list)+'\n')
#     output_file.write(str(min_make_list)+'\n')
 
#     output_file.close()
#     plt.plot(n_list, max_make_list,label='Max. Sort')
#     plt.plot(n_list, min_make_list,label='Min. Sort')

#     makespan_list = [] 
#     makespan_time_list = []
#     top_make_list = []
#     top_time_list = []

#     print top_count
#     print len(n_list)
#     return makespan_list,makespan_time_list,top_make_list,top_time_list


