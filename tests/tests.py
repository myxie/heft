#!/usr/bin/enb
"""
unittest runner for the heft.py code """
import sys
import unittest
from heft.heft import Task, Heft
from graph.graph import random_comm_matrix, random_comp_matrix,\
random_task_dag

import networkx as nx

class TestTaskMethods(unittest.TestCase):

    def test_task_equality(self):
        a = Task(1) 
        b = Task(1)
        self.assertTrue(a == b)

    def test_task_inequality(self):
        a = Task(2)
        b = Task(4)
        self.assertFalse(a == b)

    def test_task_hash(self):
        a = Task(57) 
        hashval = hash(57)
        self.assertTrue(hashval == a.__hash__())

class TestGraphMethods(unittest.TestCase):

    def test_task_networkx_add_edges(self):
        a = Task(1) 
        b = Task(2)
        digraph = nx.DiGraph()
        digraph.add_weighted_edges_from([(a, b, 2)])
        edge = digraph.edges()[0] # edges() returns list 
        self.assertTrue(edge == (a,b))

    def test_task_networkx_remove_edges(self):
        a = Task(1) 
        b = Task(2)
        c = Task(3)
        d = Task(6)
        digraph = nx.DiGraph()
        digraph.add_weighted_edges_from([(a, b, 2), (b,c,4)])
        edge = digraph.edges()[1]
        self.assertTrue(edge == (b,c))
        digraph.remove_edge(b,c)
        edges = digraph.edges()
        self.assertFalse(edge in edges)

    @unittest.skip("In Development")
    def test_random_comm_matrix(self):
        matrix = random_comm_matrix(4,10)


class TestHeftMethods(unittest.TestCase):
    
    def setUp(self):
        """
        Calc. rank by hand is a pain; the hard work is done here
        1 processor
        Task A = 0, Task B = 1 etc. 
        A comp_cost = 4
        B comp_cost = 6
        C comp_cost = 9
        D comp_cost = 3
        A->B; A->C; B->D; C->D
        """
        self.heft = Heft('tests/test_comp.txt',\
                'tests/test_comm.txt',\
                'tests/unit_test.graphml')

    def tearDown(self):
        return -1

    def test_rank_multiple_successors(self):
        nodeA = self.heft.graph.nodes()[0]
        nodeD = self.heft.graph.nodes()[3]
        self.heft.rank_up(nodeD) 
        self.heft.rank_up(nodeA) 
        self.assertTrue(nodeD.rank == 3)
        self.assertTrue(nodeA.rank == 19)

    def test_ave_comm(self):
        graph = self.heft.graph
        nodes = graph.nodes()
        cost = self.heft.ave_comm_cost(nodes[0].tid,nodes[1].tid)

    def test_ave_comp(self):
        nodeA = Task(1)
        nodeA.comp_cost = [3,2,1]

    def test_top_sort(self):
        graph = self.heft.graph
        nodes = graph.nodes()
        sorted_nodes = self.heft.top_sort_tasks()

    def test_rank_sort(self):
        sorted_nodes = self.heft.rank_sort_tasks()

    def test_calc_est(self):
        known_est_nodeA = 0
        known_est_nodeC = 0

    def test_insertion_policy(self):
        retval = self.heft.insertion_policy()
        task_sort = retval[0]

class TestHeftMethodsTopcuoglu(unittest.TestCase):
    """
    This class tests HEFT on the same example graph presented by 
    Topcuoglu et al
    """ 
     
    def setUp(self):
        return -1

    def tearDown(self):
        return -1



