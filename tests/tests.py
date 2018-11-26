#!/usr/bin/env
# Sunittest runner for the heft.py code 
import unittest
import networkx as nx
from csv import reader

import sys
sys.path.insert(0, '../heft')

from heft.heft import Task, Heft



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


class TestHeftMethodsTopcuoglu(unittest.TestCase):
    """
    This class tests HEFT on the same example graph presented by 
    Topcuoglu et al
    """ 
     
    def setUp(self):
        self.heft = Heft('tests/topcuoglu_comp.txt',\
            'tests/topcuoglu_comm.txt',\
            'tests/topcuoglu.graphml')


    def tearDown(self):
        return -1
    
    def test_rank(self):
        rank_values = [108,77,79,80,69,63,42,35,44,14]
         
        self.heft.rank('up')
        sorted_nodes = self.heft.rank_sort
        for count, node in enumerate(sorted_nodes):
            self.assertTrue(int(node.rank) == rank_values[node.tid])  
    
    def test_schedule(self):
        self.heft.rank('up')
        retval = self.heft.schedule('insertion')
        print("Makespan is: ", retval)
        self.assertTrue(retval == 80)

@unittest.skip( 'Smaller test case')                
class TestHeftMethodsOCT(unittest.TestCase):

    """
    This class tests HEFT on the same example graph presented by Arabnejad 
    and Barbos
    """
    def setUp(self):
        self.heft= Heft('tests/oct_comp.txt',\
            'tests/oct_comm.txt',\
            'tests/oct.graphml')
        self.oct_rank_values = [72,41,37,43,31,41,17,20,16,0]
        self.up_rank_values = [169,114,102,110,129,119,52,92,42,20]

    def tearDown(self):
        return -1

    def test_up_rank(self):
        self.heft.rank('up')
        sorted_nodes = self.heft.rank_sort
        for count, node in enumerate(sorted_nodes):
            self.assertTrue(int(node.rank) == self.up_rank_values[node.tid])  

    def test_oct_rank(self):
        self.heft.rank('oct')
        sorted_nodes = self.heft.rank_sort
        for count, node in enumerate(sorted_nodes):
            self.assertTrue(int(node.rank) == self.oct_rank_values[node.tid])  
    
    @unittest.skip('Unnecessary')
    def test_oct_matrix(self):
        self.heft.rank('oct')
        for key in self.heft.oct_rank_matrix:
            print(key, self.heft.oct_rank_matrix[key])
        
    def test_heft_schedule(self):
        self.heft.rank('up')
        retval = self.heft.schedule('insertion')
        self.assertTrue(retval == 133)

    def test_oct_schedule(self):
        self.heft.rank('oct')
        retval = self.heft.schedule('oct_schedule')
        self.assertTrue(retval == 122)

       


