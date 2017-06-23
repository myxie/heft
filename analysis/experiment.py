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
from heft.heft import Heft
from heft.graph import create_processors, random_task_dag,random_comp_matrix,random_comm_matrix 
from heft.task import Task
import networkx as nx

import matplotlib.pyplot as plt


def setup_graph():

    """
    We need: 
    Graph
    Computation matrix
    communication matrix
    Heft object 
    """

    graph = nx.DiGraph()
    a,b,c,d,e,f =  Task(0),Task(1),Task(2),Task(3),Task(4),Task(5)
    graph.add_nodes_from([a,b,c,d,e,f])
    graph.add_edges_from([(a,b ),(a,c),(b,e),(c,d),(d,e),(e,f)])

    comp_matrix={0:[7,5],1:[8,9],2:[4,15],3:[2,1],4:[8,5],5:[12,11]}

    comm_matrix=[[0,7,12,0,0,0],[7,0,0,0,5,0],[12,0,0,6,0,0],\
        [0,0,0,0,11,0],[0,5,0,11,0,9],[0,0,0,0,9,0]]

    processors = create_processors(2)

    heft = Heft(graph,comm_matrix,comp_matrix,processors)
    heft.rank_up(graph.nodes()[0])
    #print    heft.top_sort_tasks()
    for task in  heft.rank_sort_tasks():
        print 'taskid: ' + str(task.tid) + ': '+ str(task.rank)
    makespan_tuple = heft.insertion_policy()
    for x in range(len(makespan_tuple[1])):
        print makespan_tuple[1][x]


def run_random_heft():
    """
    This runs the HEFT algorithm on an increasing number of nodes 
    and adds each makespan onto a list 
    """
    nodes_init=10
    nodes_final=1001
    makespan_list = [] 
    makespan_time_list = []
    makespan_rank_time = []
    makespan_insertion_time = []
    top_make_list = []
    top_time_list = []
    # difference_list = []
    num_processor = 2
    #,2,3,4,5,3,4,5
    n_list = [x for x in range(nodes_init,nodes_final,50)]
    for x in [(4/float(3)),2,3,4,5]:   
        for n in range(nodes_init, nodes_final, 50):
            g = random_task_dag(n,float(x*n))
            # p = create_processors(num_processor)
            comp = random_comp_matrix(num_processor,n,20)
            comm = random_comm_matrix(n,10)
            heft = Heft(g,comm,comp,num_processor)
            makespan_tuple = heft.makespan()
            makespan_list.append(makespan_tuple[0])
            makespan_time_list.append(makespan_tuple[1])
            # makespan_rank_time.append(makespan_tuple[2])
            # makespan_insertion_time.append(makespan_tuple[3])
            topmakespan_tuple = heft.top_makespan()
            top_make_list.append(topmakespan_tuple[0])
            top_time_list.append(topmakespan_tuple[1])
        
        # plt.plot(n_list, makespan_list,label=str(1/(float(x))))
        # print zip(top_make_list,makespan_list)
        # print [i-j for i,j in zip(top_make_list,makespan_list)]
        # difference_list = [i - j for i, j in zip(top_make_list, makespan_list)]
        output_file = open('output.txt','a')
        output_file.write(str(makespan_time_list)+'\n')
        output_file.write(str(top_time_list)+'\n')
        output_file.write('******************************************************\n')
        output_file.close()
        plt.plot(n_list, makespan_time_list,label='Makespan: ' +str(1/float(x)))
        plt.plot(n_list, top_time_list , label= 'Top: ' + str(1/float(x)))

        #plt.plot(n_list,makespan_time_list,label='Total')
        # plt.plot(n_list,makespan_rank_time,label='Rank')
        # plt.plot(n_list,makespan_insertion_time,label='Insertion')
        # plt.plot(n_list,top_time_list,label='Top')
        makespan_list = [] 
        makespan_time_list = []
        top_make_list = []
        top_time_list = []

    plt.legend()
    plt.show()

    return makespan_list,makespan_time_list,top_make_list,top_time_list

#TODO Change this to produce a nicer output
def rank_heft():
    nodes_init=10
    nodes_final=1000
    makespan_list = [] 
    makespan_time_list = []
    makespan_rank_time = []
    makespan_insertion_time = []
    top_make_list = []
    top_time_list = []
    max_make_list = []
    min_make_list = []
    # difference_list = []
    num_processor = 2
    #,2,3,4,5,3,4,5
    max_count = 0
    min_count =0
    top_count = 0
    n_list = [x for x in range(nodes_init,nodes_final,50)]
    # for x in [(4/float(3)),2,3,4,5]:   
    for n in range(nodes_init, nodes_final, 50):
        g = random_task_dag(n,float(2*n))
        p = create_processors(num_processor)
        comp = random_comp_matrix(num_processor,n,20)
        comm = random_comm_matrix(n,10)
        heft = Heft(g,comm,comp,num_processor)
        # top_heft = Heft(g,comm,comp,num_processor)

        makespan_tuple = heft.makespan()
        makespan_list.append(makespan_tuple[0])
        # makespan_time_list.append(makespan_tuple[1])
        # # makespan_rank_time.append(makespan_tuple[2])
        # # makespan_insertion_time.append(makespan_tuple[3])
        topmakespan_tuple = heft.top_makespan()
        top_make_list.append(topmakespan_tuple[0])
        # # top_time_list.append(topmakespan_tuple[1])
        
        maxmakespan_tuple = heft.max_makespan()
        max_make_list.append(maxmakespan_tuple[0])
        minmakespan_tuple = heft.min_makespan()
        min_make_list.append(minmakespan_tuple[0])

        if (makespan_tuple[0] < maxmakespan_tuple[0]):
            max_count = max_count + 1
        if (makespan_tuple[0] < minmakespan_tuple[0]):
            min_count = min_count + 1
        if (makespan_tuple[0] < topmakespan_tuple[0]):
            top_count = top_count + 1

    plt.plot(n_list, makespan_list,label='Rank Sort')
    plt.plot(n_list, top_make_list,label='Rank Sort')

    output_file = open('output.txt','a')
    output_file.write(str(makespan_list)+'\n')
    output_file.write(str(top_make_list)+'\n')
    output_file.write(str(max_make_list)+'\n')
    output_file.write(str(min_make_list)+'\n')
 
    output_file.close()
    plt.plot(n_list, max_make_list,label='Max. Sort')
    plt.plot(n_list, min_make_list,label='Min. Sort')

    makespan_list = [] 
    makespan_time_list = []
    top_make_list = []
    top_time_list = []

    print top_count
    print len(n_list)
    return makespan_list,makespan_time_list,top_make_list,top_time_list


       


if __name__ == '__main__':
    #setup_graph()
    print run_random_heft()
    #rank_heft()
