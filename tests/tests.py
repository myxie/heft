#!/usr/bin/env
# Sunittest runner for the heft.py code 
import sys
import unittest
from heft.heft import Task, Heft
from graph.graph import random_comm_matrix, random_comp_matrix,\
random_task_dag

import networkx as nx

matrix_path = ''
graph_path=''

class TestTaskMethods(unittest.TestCase):

    def test_task_equality(self):
        a = Task(1) 
        b = Task(1)
        self.assertTrue(a == b)

    def test_task_inequality(self):
        a = Task(2)
        b = Task(4)
        self.assertFalse(a == b)

    def test_task_greater(self):
        a = Task(2)
        b = Task(2)
        self.assertTrue(b <= a)

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
        edge = list(digraph.edges())[0] # edges() returns list 
        self.assertTrue(edge == (a,b))

    def test_task_networkx_remove_edges(self):
        a = Task(1) 
        b = Task(2)
        c = Task(3)
        d = Task(6)
        digraph = nx.DiGraph()
        digraph.add_weighted_edges_from([(a, b, 2), (b,c,4)])
        edge = list(digraph.edges())[1]
        self.assertTrue(edge == (b,c))
        digraph.remove_edge(b,c)
        edges = list(digraph.edges())
        self.assertFalse(edge in edges)

    @unittest.skip("In Development")
    def test_random_comm_matrix(self):
        matrix = random_comm_matrix(4,10)

@unittest.skip("In Development")
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
        return 1

    def test_insertion_policy(self): 
        retval = self.heft.insertion_policy()
        task_sort = retval

# @unittest.skip("In Development")
class TestHeftMethodsTopcuoglu(unittest.TestCase):
    """
    This class tests HEFT on the same example graph presented by 
    Topcuoglu et al
    """ 
     
    def setUp(self):
        self.heft = Heft('tests/topcuoglu_comp.txt',\
            'tests/topcuoglu_comm.txt',\
            'tests/topcuoglu.graphml')
         
        return -1

    def tearDown(self):
        return -1
    
    def test_rank(self):
        rank_values = [106,75,79,78,67,62,42,35,43,14]
#       print rank_values
         
        self.heft.rank('up')
        nodes = self.heft.graph.nodes()
        #for x in range(0,10):
#       for node in nodes:
#           print (str(node.tid) + ': '+ str(node.rank))
            #self.assertTrue(nodes[x].rank == rank_values[x])

    def test_insertion(self):
        self.heft.rank('up')
        retval = self.heft.insertion_policy()
        print ('insertion ', str(retval))

    def test_critical_path(self):
        retval = self.heft.critical_path()
        
        print ("critical_path" , str(retval))
    def test_sequential_cost(self):
        retval = self.heft.sequential_execution()
        print ("sequential_exection " , str(retval))

    def test_greedy(self):
        self.heft.rank('up')
        retval = self.heft.greedy_policy()
        print ('greedy' , str(retval))

    def test_rank_random(self):
        self.heft.rank('random')
        retval = self.heft.insertion_policy()
        print ("random rank:" , str(retval))
        
#@unittest.skip("In Development")
class TestHeftMethodsOCT(unittest.TestCase):

    """
    This class tests HEFT on the same example graph presented by Arabnejad 
    and Barbos
    """
    def setUp(self):
        self.heft= Heft('tests/oct_comp.txt',\
            'tests/oct_comm.txt',\
            'tests/oct.graphml')

        return -1

    def tearDown(self):
        return -1

    def test_oct_rank(self):
        self.heft.rank('oct')
        self.heft.show_rank()
        
    def test_oct_insertion(self):
        self.heft.rank('oct')
        retval = self.heft.schedule('oct_schedule')
        print('oct_schedule oct ', str(retval))

    def test_oct_greedy(self):
        self.heft.rank('oct')
        retval = self.heft.greedy_policy()
        
#@unittest.skip("In Development")

class TestDALiuGEBashHeft(unittest.TestCase): 

    """
    This class tests the schedule of the bash_test.json DALiuGE graph
    """

    def setUp(self):
        self.heft = Heft('/home/croutons/Dropbox/University/UWA/bsc-honours/thesis/data/input/matrices/comp_50/comp_10-2.txt',\
                '/home/croutons/Dropbox/University/UWA/bsc-honours/thesis/data/input/matrices/comm_50/comm_10.txt',\
                'tests/translated_importer.graphml')
    
    def tearDown(self):
            return -1


    @unittest.skip("In Development")
    def test_bash_ranking(self):
        self.heft.rank('oct')
            
        nodes = self.heft.graph.nodes()
#       for node in nodes:
#           print (str(node.tid) + ' :' + str(node.oct_rank))
    
    def test_bash_insertion(self):
        self.heft.rank('up')
        retval = self.heft.insertion_policy()
        print (retval) 
        #print(self.heft.processors)

class TestGenerateExampleOCTMatrix(unittest.TestCase):
    
    def test_setup_oct_graph(self):
        heft = 1

#@unittest.skip("In Development")
class TestHEFTExperiments(unittest.TestCase):

    def setUp(self):
        return -1
        #graph = nx.read_graphml(graphml,Task)

    #@unittest.skip("In Development")
    
    def test_find_appropriate_matrix(self):
        """
        We want to read in the cost matrices that correspond to the 
        the number of nodes in the graph
        """
        heft = Heft('/home/croutons/Dropbox/University/UWA/bsc-honours/thesis/data/input/matrices/comp_50/comp_130-3.txt',\
                '/home/croutons/Dropbox/University/UWA/bsc-honours/thesis/data/input/matrices/comm_50/comm_130.txt',
                '/home/croutons/Dropbox/University/UWA/bsc-honours/thesis/data/input/graphml/translated_mwa_gleam_simple.graphml')

        heft.rank('up')
        retval = heft.insertion_policy()
        print ('insertion up' , str(retval))

        return -1

#    @unittest.skip("In Development")
    def test_more_things(self):
        """
        We want to read in the cost matrices that correspond to the 
        the number of nodes in the graph
        """
        heft = Heft('/home/croutons/Dropbox/University/UWA/bsc-honours/thesis/data/input/matrices/comp_50/comp_130-3.txt',\
                '/home/croutons/Dropbox/University/UWA/bsc-honours/thesis/data/input/matrices/comm_50/comm_130.txt',
                '/home/croutons/Dropbox/University/UWA/bsc-honours/thesis/data/input/graphml/translated_mwa_gleam_simple.graphml')

        heft.rank('oct')
        #heft.show_rank()
        retval = heft.insertion_policy()
        print ('oct insertion' , str(retval))
        #for tpl in sorted(heft.oct_rank_matrix.keys()):
        #    print "%s: %s" % (tpl, heft.oct_rank_matrix[tpl])
    def test_more_things_greedy_oct(self):

        heft = Heft('/home/croutons/Dropbox/University/UWA/bsc-honours/thesis/data/input/matrices/comp_50/comp_130-3.txt',\
                '/home/croutons/Dropbox/University/UWA/bsc-honours/thesis/data/input/matrices/comm_50/comm_130.txt',
                '/home/croutons/Dropbox/University/UWA/bsc-honours/thesis/data/input/graphml/translated_mwa_gleam_simple.graphml')

        heft.rank('oct')
        #heft.show_rank()
        retval = heft.greedy_policy()
        print ('oct greedy' , str(retval))

        #retval = heft.insertion_policy()
        #print 'insertion ' + str(retval[2])

        return -1
    def test_greedy_find_appropriate_matrix(self):
        """
        We want to read in the cost matrices that correspond to the 
        the number of nodes in the graph
        """
        heft = Heft('/home/croutons/Dropbox/University/UWA/bsc-honours/thesis/data/input/matrices/comp_50/comp_130-3.txt',\
                '/home/croutons/Dropbox/University/UWA/bsc-honours/thesis/data/input/matrices/comm_50/comm_130.txt',
                '/home/croutons/Dropbox/University/UWA/bsc-honours/thesis/data/input/graphml/translated_mwa_gleam_simple.graphml')

        heft.rank('up')
        retval = heft.greedy_policy()
        print ('greedy up' , str(retval))

        return -1


