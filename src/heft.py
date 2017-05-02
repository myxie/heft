"""
Functions for static HEFT implementation
"""
import networkx as nx
import task 

"""
HEFT is organised into 2 phases: 

    - Task Prioritisation
    - Processor Allocation

In this Implementation of HEFT, we are testing the difference between a 
topological sort and the original ranku function implemented in HEFT.
For more information, read the original paper here: 

Variables: 

v = set of vertices
e = set of edges

Data - v x v matrix of communication data. Data(i,k) is the amount of data
required to be transmittied from ni to nk (where n is a given task)

Q - set of heterogeneous resources 'q'. Interprocessor communication is assumed
to occur without communication.

W - computation cost matrix (w = work...I think). W(i,j) gives the time cost 
of task ni on processor pj

B - transfer rates matrix (between processors). I.e. B(m,n) gives the 
(predicted) transfer rate between processor pm and pn.

Communication cost from edge (i,k), transferring data from task ni to nk 
(from pm to pn respectively), is given by:

C(i,k) = data(i,k)/B(m,n) + L(m),

Where L(m) is the startup communication cost on pm.

C(i,k) = 0 when pn = pm.
"""


def ave_comm_cost(node,successor):
    return 5 

def ave_comp_cost(node,successor):
    return -1 

def calc_eft(graph):
    return -1

def calc_est(graph):
    return -1

def rank_up(node,graph):
    """
    Upward ranking heuristic outlined in Topcuoglu, Hariri & Wu (2002)
    Closely modelled off 'cal_up_rank' function at: 
    https://github.com/oyld/heft/blob/master/src/heft.py

    :param node: A task node in an DAG that is being ranked
    :param graph: A DAG - contains successor information about nodes 
    """

    longest_rank = 0
    for successor in graph.successors(node):
        print successor
        if successor.rank is -1:
            rank_up(successor,graph)

        longest_rank = max(longest_rank, ave_comm_cost(node,successor)+ successor.rank)

    node.rank = node.ave_comp + longest_rank
    print node.rank

def rank_sort_tasks(graph):
    """
    Model from this: http://stackoverflow.com/questions/403421/how-to-sort-a-list-of-objects-based-on-an-attribute-of-the-objects
    ut.sort(key=lambda x: x.count, reverse=True)
    
    Sort Tasks by rank provided. According to Topcuolgu, Hariri & Wu (2002), 
    this is a topological order of tasks
    """
    return -1 

def top_sort_tasks(graph):
    """
    Use networkx library built-in topological sort function to generate a sorted
    list of tasks based on precedence constraints. This is to test whether or not 
    the ranking heuristic is any better than a topological sort approach
    """

# if __name__ == '__main__':
  
