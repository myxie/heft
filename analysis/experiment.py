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

    comp_matrix={0:[7,5],1:[8,9],2:[4,16],3:[2,1],4:[8,5],5:[12,11]}

    comm_matrix=[[0,7,12,0,0,0],[7,0,0,0,5,0],[12,0,0,6,0,0],\
        [0,0,0,0,11,0],[0,5,0,11,0,9],[0,0,0,0,9,0]]

    processors = create_processors(2)

    heft = Heft(graph,comm_matrix,comp_matrix,processors)
    heft.rank_up(graph.nodes()[0])
    for task in  heft.rank_sort_tasks():
        print str(task.tid) + ': ' + str(task.rank)

def run_random_heft():
    """
    This runs the HEFT algorithm on an increasing number of nodes 
    and adds each makespan onto a list 
    """
    nodes_init=10
    nodes_final=101
    makespan_list = [] 
    top_make_list = []
    num_processor = 2
    for n in range(nodes_init, nodes_final, 10):
        g = random_task_dag(n,2*n)
        p = create_processors(num_processor)
        comp = random_comp_matrix(num_processor,n,20)
        comm = random_comm_matrix(n,10)
        heft = Heft(g,comm,comp,p)
        makespan = heft.makespan()
        topmakespan=heft.top_makespan()
        makespan_list.append(makespan)
        top_make_list.append(topmakespan)
    return makespan_list,top_make_list

if __name__ == '__main__':
    #setup_graph()
    print run_random_heft()
