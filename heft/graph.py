# Functions associated with creating a Graph that can be used in the HEFT algorithm


import networkx as nx
from task import Task
import random

def create_processors(processors):
    """
    Function that creates a given number of processors
    
    :param processors: The number of processors 
    """
    processor_dict = dict() 
    for x in range(0,processors):
        processor_dict[x]=[] 

    return processor_dict

def random_comp_matrix(processors, nodes, cost):
    """
    Function that generates a random cost matrix for a number of tasks
    
    :param processors: Number of processors available
    :param nodes: Number of nodes with costs
    :param cost: A range that determines the maximum random cost that can be generated
    """
    
    # For each processor, we have a list of nodes with computation/communication costs 
    computation_matrix = dict()

    for x in range(nodes):
        computation_matrix[x] = random.sample(range(cost),processors)
    
    return computation_matrix


def random_comm_matrix(nodes, cost):
    """
    Function that generates a random communication cost (n x n) matrix for a number of tasks
    
    :param nodes: Number of nodes with costs
    :param cost: A range that determines the maximum random cost that can be generated
    """
    
    # For each processor, we have a list of nodes with communication costs 
    #communication_matrix = dict()
    communication_matrix = [[0 for x in range(nodes)] for x in range(nodes)] 
    for x in range(nodes-1):
        for y in range(x+1,nodes):
            communication_matrix[x][y]=random.randint(0,cost)
            communication_matrix[y][x]=communication_matrix[x][y]

    return communication_matrix

def init_tasks(graph, comp_matrix):
    for task in graph:
         task.comp_cost = comp_matrix[task.tid]    
 

def random_task_dag(nodes, edges):
    """Generate a random Directed Acyclic Graph (DAG) with a given number of nodes and edges.
    Modified from source: http://ipyparallel.readthedocs.io/en/latest/dag_dependencies.html
    """
    graph = nx.DiGraph()
    count = 0
    if nodes is 1:
        return graph
    for i in range(nodes):
        graph.add_node(Task(i))
    while edges > 0:
        a = Task(random.randint(0,nodes-1))
        b=a
        while b==a:
            b = Task(random.randint(0,nodes-1))
        graph.add_edge(a,b)
        if nx.is_directed_acyclic_graph(graph):
            edges -= 1
        else:
            # we closed a loop!
            graph.remove_edge(a,b)
    return graph

if __name__ == "__main__":
    """
    Working with graphs
    """
    num_processors=3
    nodes=5 
    edges=6

#   comp_matrix = random_cost_matrix(processors, nodes,100) 
#   comm_matrix = random_cost_matrix(node, nodes,50) # Node x Node communication matrix
    processors = create_processors(num_processors)
    graph = random_task_dag(nodes,edges)

        
