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

    def test_random_comm_matrix(self):
        matrix = random_comm_matrix(4,10)

    #unittest.skip("Skipping Heft Until re-organise class structure")

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
        self.heft = Heft('graph/matrices/test_comp.txt',\
                'graph/matrices/test_comm.txt',\
                'graph/graphml/unit_test.graphml')

    def tearDown(self):
        return -1

    @unittest.skip("Skipping Heft Until re-organise class structure")
    def test_rank_no_successors(self):
        G = nx.DiGraph()
        T1 = Task(1)
        T1.ave_comp = 5
        G.add_node(T1)
        rank_up(T1,G)
        self.assertTrue(T1.rank == 5)
        #TODO Add a few tasks to the digraph and choose one with and without successors

    @unittest.skip("Skipping Heft Until re-organise class structure")
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
        nodeA = self.heft.graph.nodes()[0]
        nodeD = self.heft.graph.nodes()[3]
        #self.heft.rank_up(nodeD) 
        self.heft.rank_up(nodeA) 
        self.assertTrue(nodeD.rank == 3)
        self.assertTrue(nodeA.rank == 19)
    #@unittest.skip("Skipping Heft Until re-organise class structure")

    def test_ave_comm(self):
        graph = self.heft.graph
        nodes = graph.nodes()
        cost = self.heft.ave_comm_cost(nodes[0].tid,nodes[1].tid)

    # @unittest.skip("Skipping Heft Until re-organise class structure")
    def test_ave_comp(self):
        nodeA = Task(1)
        nodeA.comp_cost = [3,2,1]
        #print self.heft.ave_comp_cost(nodeA.tid)


    # @unittest.skip("Skipping Heft Until re-organise class structure")
    def test_top_sort(self):
        graph = self.heft.graph
        nodes = graph.nodes()
        sorted_nodes = self.heft.top_sort_tasks()
    # @unittest.skip("Skipping Heft Until re-organise class structure")    
    def test_rank_sort(self):
        sorted_nodes = self.heft.rank_sort_tasks()
        for node in sorted_nodes:
            print 'Node-id: ' + str(node.tid) + ' rank: ' + str(node.rank)
    # @unittest.skip("Skipping Heft Until re-organise class structure")    
    def test_calc_est(self):
        known_est_nodeA = 0
        known_est_nodeC = 0
    # @unittest.skip("Skipping Heft Until re-organise class structure")
    def test_insertion_policy(self):
        retval = self.heft.insertion_policy()
        task_sort = retval[0]
        for task in task_sort:
            print 'Processor No. ' + str(task.processor)
        print retval[1]
         
class TestMoreHeftMethods(unittest.TestCase):

    @unittest.skip("Skipping  Heft Until re-organise class structure")

    def test_random_rank(self):
        num_nodes = 10
        num_edges = 20
        num_processors = 3
        heft_g = Heft(num_nodes,num_processors,20)
        nodeB = heft_g.graph.nodes()[1]
        print '***Comms***'
        retval = heft_g.insertion_policy()
        task_sort = retval[0]
        print '***Predecessors***'
        for node in heft_g.graph.nodes():
            print 'Node tid: ' + str(node.tid) + ': ' + str(heft_g.graph.predecessors(node))
        for task in task_sort:
            print 'id: ' + str(task.tid) + 'rank: ' +str(task.rank) + 'aft: ' + str(task.aft)
        for x in range(len(retval[1])):
            print retval[1][x]
        print retval[2]
        print heft_g.graph.nodes()[nodeB.tid]

