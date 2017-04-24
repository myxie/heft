
#working out the graph strucutre for the HEFT algorithm


import networkx as nx
from heft import Task
from draw import draw_graph

if __name__ == '__main__':
    """
    Working with graphs
    """
    task_1 = Task(1) 
    task_2 = Task(2)
    task_3 = Task(3)
    digraph = nx.DiGraph()
    digraph.add_weighted_edges_from([(task_1, task_2, 2),(task_1,task_3,4)])
    # print digraph.successors(task_1)[0].tid
    draw_graph(digraph)

        