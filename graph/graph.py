# Functions associated with creating a Graph that can be used in the HEFT algorithm

# Copyright (C) 2017 RW Bunney

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.  
import random
import os

import networkx as nx

from heft.heft import Task


def random_comp_matrix(processors, nodes, lower, upper):
	"""
    Function that generates a random cost matrix for a number of tasks
    
    :param processors: Number of processors available
    :param nodes: Number of nodes with costs
    :param cost: A range that determines the maximum random cost that can be generated
    """

	# For each processor, we have a list of nodes with computation/communication costs 
	computation_matrix = dict()

	for x in range(nodes):
		computation_matrix[x] = random.sample(range(lower, upper), processors)
	if not os.path.isdir('/home/artichoke/Dropbox/thesis/data/input/matrices/comp_{0}/'.format(upper)):
		os.makedirs('/home/artichoke/Dropbox/thesis/data/input/matrices/comp_{0}/'.format(upper))
	name = '/home/artichoke/Dropbox/thesis/data/input/matrices/comp_{0}/comp_{1}-{2}.txt'.format(upper, nodes,
																								 processors)
	file = open(name, 'w')
	file.write("P1,P2,...,Pn\n")
	for n in range(len(computation_matrix)):
		file.write(str(computation_matrix[n]) + '\n')
	file.close()

	return computation_matrix


def random_comm_matrix(nodes, lower, upper):
	"""
	Function that generates a random communication cost (n x n) matrix for a number of tasks
	:param nodes: Number of nodes with costs
	:param cost: A range that determines the maximum random cost that can be generated
	"""
	# For each processor, we have a list of nodes with communication costs 
	# communication_matrix = dict()
	communication_matrix = [[0 for x in range(nodes)] for x in range(nodes)]
	for x in range(nodes - 1):
		for y in range(x + 1, nodes):
			communication_matrix[x][y] = random.randint(lower, upper)
			communication_matrix[y][x] = communication_matrix[x][y]
			print(communication_matrix[x][y])
	if not os.path.isdir('/home/artichoke/Dropbox/thesis/data/input/matrices/comm_{0}/'.format(upper)):
		os.makedirs('/home/artichoke/Dropbox/thesis/data/input/matrices/comm_{0}/'.format(upper))
	name = '/home/artichoke/Dropbox/thesis/data/input/matrices/comm_{0}/comm_{1}.txt'.format(upper, nodes)
	file = open(name, 'w')
	file.write("N1,N2,...,Nx\n")
	for n in range(len(communication_matrix)):
		file.write(str(communication_matrix[n]) + '\n')
	file.close()

	return communication_matrix


def random_task_dag(nodes, edges):
	"""
	Generate a random Directed Acyclic Graph (DAG) with a given number of nodes and edges.
	Modified from source: http://ipyparallel.readthedocs.io/en/latest/dag_dependencies.html
	"""
	graph = nx.DiGraph()
	count = 0
	if nodes is 1:
		return graph
	for i in range(nodes):
		graph.add_node(Task(i))
	graph.add_edge(Task(0), Task(1))
	while edges > 0:
		a = Task(random.randint(0, nodes - 1))
		b = a
		while b.tid == a.tid:
			b = Task(random.randint(1, nodes - 1))
		if b.tid > 0 and a >= 0:
			graph.add_edge(a, b)
			if nx.is_directed_acyclic_graph(graph):
				edges -= 1
			else:
				# we closed a loop!
				graph.remove_edge(a, b)
		else:
			continue

	node_list = graph.nodes()
	count = 1
	for node in node_list:
		if node.tid != 0:
			predecessors = graph.predecessors(node)
			while predecessors is []:
				new_task = random.randint(1, nodes - 1)
				graph.add_edge(new_task, node)
				if nx.is_directed_acyclic_graph(graph):
					predecessors = graph.predecessors(node)
				else:
					graph.remove_edge(new_task, node)
		else:
			continue

	return graph


def gen_test_graph():
	# Calc. rank by hand is a pain; the hard work is done here
	# 1 processor
	# Task A = 0, Task B = 1 etc. 
	# A comp_cost = 4
	# B comp_cost = 6
	# C comp_cost = 9
	# D comp_cost = 3
	# A->B; A->C; B->D; C->D
	nodes = [Task(x) for x in range(4)]

	graph = nx.DiGraph()
	graph.add_nodes_from(nodes)
	# init_tasks(graph,comp_matrix)
	graph.add_edge(nodes[0], nodes[1])  # A->B
	graph.add_edge(nodes[0], nodes[2])  # A->C
	graph.add_edge(nodes[1], nodes[3])  # B->D
	graph.add_edge(nodes[2], nodes[3])  # C->D
	comm = {0: [0, 1, 1, 0], 1: [0, 0, 0, 2], 2: [0, 0, 0, 2], 3: [0, 0, 0, 0]}
	comp = {0: [4, 4], 1: [6, 6], 2: [9, 9], 3: [3, 3]}

	file = open('test_comp.txt', 'w')
	file.write("P1,P2,...,Pn\n")
	for n in range(len(comp)):
		file.write(str(comp[n]) + '\n')
	file.close()

	file = open('test_comm.txt', 'w')
	file.write("N1,N2,...,Nn\n")
	for n in range(len(comm)):
		file.write(str(comm[n]) + '\n')
	file.close()

	nx.write_graphml(graph, "unit_test.graphml")
	print('Test' + str(graph.nodes()))
	return graph


def gen_oct_graph():
	comp = {0: [22, 21, 36], 1: [22, 18, 18],
			2: [32, 27, 43], 3: [7, 10, 4],
			4: [29, 27, 35], 5: [26, 17, 24],
			6: [14, 25, 30], 7: [29, 23, 36],
			8: [15, 21, 8], 9: [13, 16, 33]}
	comm = {0: [0, 17, 31, 29, 13, 7, 0, 0, 0, 0],
			1: [17, 0, 0, 0, 0, 0, 0, 3, 30, 0],
			2: [31, 0, 0, 0, 0, 0, 16, 0, 0, 0],
			3: [29, 0, 0, 0, 0, 0, 0, 11, 7, 0],
			4: [13, 0, 0, 0, 0, 0, 0, 0, 57, 0],
			5: [7, 0, 0, 0, 0, 0, 0, 5, 0, 0],
			6: [0, 0, 16, 0, 0, 0, 0, 0, 0, 9],
			7: [0, 3, 0, 11, 0, 5, 0, 0, 0, 42],
			8: [0, 30, 0, 7, 57, 0, 0, 0, 0, 7],
			9: [0, 0, 0, 0, 0, 0, 0, 9, 42, 7]}

	graph = nx.DiGraph()
	file = open('oct_comp.txt', 'w')
	file.write("P1,P2,...,Pn\n")
	for n in range(len(comp)):
		file.write(str(comp[n]) + '\n')
	file.close()

	file = open('oct_comm.txt', 'w')
	file.write("N1,N2,...,Nn\n")
	for n in range(len(comm)):
		file.write(str(comm[n]) + '\n')
	file.close()

	nodes = [Task(x) for x in range(0, 10)]
	graph = nx.DiGraph()
	graph.add_nodes_from(nodes)

	for node in nodes[1:6]:
		graph.add_edge(nodes[0], node)

	graph.add_edge(nodes[1], nodes[7])
	graph.add_edge(nodes[1], nodes[8])
	graph.add_edge(nodes[2], nodes[6])
	graph.add_edge(nodes[3], nodes[7])
	graph.add_edge(nodes[3], nodes[8])
	graph.add_edge(nodes[4], nodes[8])
	graph.add_edge(nodes[5], nodes[7])

	for node in nodes[6:9]:
		graph.add_edge(node, nodes[9])

	print(grape.edges())

	file = nx.write_graphml(graph, "tests/oct.graphml")
	return -1


def gen_topcuoglu_graph():
	comp = {0: [14, 16, 9], 1: [13, 19, 18],
			2: [11, 13, 19], 3: [13, 8, 17],
			4: [12, 13, 10], 5: [13, 16, 9],
			6: [7, 15, 11], 7: [5, 11, 14],
			8: [18, 12, 20], 9: [21, 7, 16]}
	comm = {0: [0, 18, 12, 9, 11, 14, 0, 0, 0, 0],
			1: [18, 0, 0, 0, 0, 0, 0, 19, 16, 0],
			2: [12, 0, 0, 0, 0, 0, 23, 0, 0, 0],
			3: [9, 0, 0, 0, 0, 0, 0, 27, 23, 0],
			4: [11, 0, 0, 0, 0, 0, 0, 0, 13, 0],
			5: [14, 0, 0, 0, 0, 0, 0, 15, 0, 0],
			6: [0, 0, 23, 0, 0, 0, 0, 0, 0, 17],
			7: [0, 19, 0, 27, 0, 15, 0, 0, 0, 11],
			8: [0, 16, 0, 23, 13, 0, 0, 0, 0, 13],
			9: [0, 0, 0, 0, 0, 0, 0, 17, 11, 13]}

	file = open('topcuoglu_comp.txt', 'w')
	file.write("P1,P2,...,Pn\n")
	for n in range(len(comp)):
		file.write(str(comp[n]) + '\n')
	file.close()

	file = open('topcuoglu_comm.txt', 'w')
	file.write("N1,N2,...,Nn\n")
	for n in range(len(comm)):
		file.write(str(comm[n]) + '\n')
	file.close()

	nodes = [Task(x) for x in range(0, 10)]
	graph = nx.DiGraph()
	graph.add_nodes_from(nodes)

	for node in nodes[1:6]:
		graph.add_edge(nodes[0], node)

	graph.add_edge(nodes[1], nodes[7])
	graph.add_edge(nodes[1], nodes[8])
	graph.add_edge(nodes[2], nodes[6])
	graph.add_edge(nodes[3], nodes[7])
	graph.add_edge(nodes[3], nodes[8])
	graph.add_edge(nodes[4], nodes[8])
	graph.add_edge(nodes[5], nodes[7])

	for node in nodes[6:9]:
		graph.add_edge(node, nodes[9])

	print(graph.edges())

	file = nx.write_graphml(graph, "tests/topcuoglu.graphml")


def seq_task_dag(nodes):
	"""
	Generate a sequential Directed Acyclic Graph (DAG) with a given number of nodes and edges.
	"""
	graph = nx.DiGraph()
	for i in range(nodes):
		graph.add_node(i)

	for i in range(nodes - 1):
		graph.add_edge(i, i + 1)

	return graph


if __name__ == "__main__":
	"""
	Working with graphs
	"""

	gen_oct_graph()
