
#working out the graph strucutre for the HEFT algorithm


import networkx as nx
from task import Task
from draw import draw_graph
from random import randint
from helper import run_random_dag
import matplotlib.pyplot as plt
import time



class HeftGraph(object):

    def __init__(self, nodes, processors):
        """
        Initialise the variables required for a graph

        :param nodes: The number of nodes in the graph
        :param processors: The number of processors available
        """
        self.comp_matrix = []
        self.comm_matrix = []
        self.graph = [] #random_task_dag()

    def _comp_matrix(self, nodes, processors):
        """
        Function that generates a random cost matrix for a number of tasks
        """
        return []

    def _comm_matrix(self):
        return []

    def _graph_init(self):
        """
        This takes a graph of n-nodes and edges and initialise
        """
        test = _comm_matrix()
        return -1


def random_dag(nodes, edges):
    """Generate a random Directed Acyclic Graph (DAG) with a given number of nodes and edges.
    Modified from source: http://ipyparallel.readthedocs.io/en/latest/dag_dependencies.html
    """
    #TODO Add weights in the random DAG
    G = nx.DiGraph()
    count = 0
    for i in range(nodes):
        G.add_node(i)
    while edges > 0:
        a = randint(0,nodes-1)
        b=a
        while b==a:
            b = randint(0,nodes-1)
        G.add_edge(a,b)
        if nx.is_directed_acyclic_graph(G):
            edges -= 1
        else:
            # we closed a loop!
            G.remove_edge(a,b)
    return G


def random_task_dag(nodes, edges):
    """Generate a random Directed Acyclic Graph (DAG) with a given number of nodes and edges.
    Modified from source: http://ipyparallel.readthedocs.io/en/latest/dag_dependencies.html
    """
    #TODO Add weights in the random DAG
    G = nx.DiGraph()
    count = 0
    if nodes is 1:
        return G
    for i in range(nodes):
        G.add_node(Task(i))
    while edges > 0:
        a = Task(randint(0,nodes-1))
        b=a
        while b==a:
            b = Task(randint(0,nodes-1))
        G.add_edge(a,b)
        if nx.is_directed_acyclic_graph(G):
            edges -= 1
        else:
            # we closed a loop!
            G.remove_edge(a,b)
    return G


if __name__ == '__main__':
    """
    Working with graphs
    """
    hg = HeftGraph(1,2)
    G = random_task_dag(1,2)  
    #nx.draw(G, with_labels=True)
    #plt.show()
        