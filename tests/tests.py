#!/usr/bin/enb
"""
unittest runner for the heft.py code 
"""
import sys
import unittest
from src.task import Task
from src.heft import rank_up

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




class TestHeftMethods(unittest.TestCase):

    def test_rank_no_successors(self):
        G = nx.DiGraph()
        T1 = Task(1)
        T1.ave_comp = 5
        G.add_node(T1)
        rank_up(T1,G)
        self.assertTrue(T1.rank == 5)
        #TODO Add a few tasks to the digraph and choose one with and without successors

    def test_rank_one_successor(self):
        G = nx.DiGraph()
        T1 = Task(1)
        T1.ave_comp = 5
        G.add_node(T1)
        T2 = Task(2)
        T2.ave_comp = 7
        G.add_node(T2)
        G.add_edge(T1,T2)
        rank_up(T1,G)
        self.assertTrue(T2.rank == 7)
        self.assertTrue(T1.rank == 17)

    def test_rank_multiple_successors(self):
        G = nx.DiGraph()
        T1 = Task(1)
        T1.ave_comp = 4
        G.add_node(T1)
        T2 = Task(2)
        T2.ave_comp = 6
        G.add_node(T2)
        G.add_edge(T1,T2)
        T3 = Task(3)
        T3.ave_comp = 9
        G.add_node(T3)
        G.add_edge(T1,T3)
        T4 = Task(4)
        T4.ave_comp = 3

        G.add_edge(T2,T4)
        G.add_edge(T3, T4)
        rank_up(T1,G)
        self.assertTrue(T4.rank == 3)
        self.assertTrue(T1.rank == 26)


    def test_another_heft_thing(self):
        return -1

"""
class TestGraphMethods(unittest.TestCase):

    def test_graph_thing(self):
        return -1

"""
