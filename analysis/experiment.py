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
from heft.graph import create_processors
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
    graph.add_nodes_from(['A', 'B','C','D','E','F'])
    graph.add_edges_from([('A', 'B'),('A','C'),('B','E'),\
    ('C','D'),('D','E'),('E','F')])

    comp_matrix={'A':[7,5],'B':[8,9],'C':[4,16],'D':[2,1],\
    'E':[8,5],'F':[12,11]}

    comm_matrix=[[0,7,12,0,0,0],[7,0,0,0,5,0],[12,0,0,6,0,0],\
        [0,0,0,0,11,0],[0,5,0,11,0,0],[0,0,0,0,9,0]]

    processors = create_processors(2)

    heft = Heft(graph,comm_matrix,comp_matrix,processors)
    heft.rank_up(graph.nodes()[0])
    heft.rank_sort_tasks()
