"""
Functions for static HEFT implementation
"""
import networkx as nx
import task 

"""
HEFT is organised into 2 phases: 

    - Task Prioritisation
    - Processor Allocation

In this Implementation of HEFT, we are testing the difference between a 
topological sort and the original ranku function implemented in HEFT.
For more information, read the original paper here: 

Variables: 

v = set of vertices
e = set of edges

Data - v x v matrix of communication data. Data(i,k) is the amount of data
required to be transmittied from ni to nk (where n is a given task)

Q - set of heterogeneous resources 'q'. Interprocessor communication is assumed
to occur without communication.

W - computation cost matrix (w = work...I think). W(i,j) gives the time cost 
of task ni on processor pj

B - transfer rates matrix (between processors). I.e. B(m,n) gives the 
(predicted) transfer rate between processor pm and pn.

Communication cost from edge (i,k), transferring data from task ni to nk 
(from pm to pn respectively), is given by:

C(i,k) = data(i,k)/B(m,n) + L(m),

Where L(m) is the startup communication cost on pm.

C(i,k) = 0 when pn = pm.
"""

class Heft(object):
    def __init__(self, graph, comm, comp,processors):
        self.graph = graph
        self.comm_matrix = comm
        self.comp_matrix = comp
        self.processors = processors 
        #print self.graph.nodes()[0].comp_cost        
        self.rank_up(self.graph.nodes()[0])

    def ave_comm_cost(self,node,successor):
        """
        Returns the 'average' communication cost, which is just 
        the cost in the matrix. Not sure how the ave. in the 
        original paper was calculate or represented...
            
        :params node: Starting node
        :params successor: Node with which the starting node is communicating
        """

        cost = self.comm_matrix[node.tid][successor.tid]
        return cost 

    def ave_comp_cost(self,tid):
        comp = self.comp_matrix[tid]
        return sum(comp)/len(comp)

    def rank_up(self,node):
        """
        Upward ranking heuristic outlined in Topcuoglu, Hariri & Wu (2002)
        Closely modelled off 'cal_up_rank' function at: 
        https://github.com/oyld/heft/blob/master/src/heft.py

        :param node: A task node in an DAG that is being ranked
        :param graph: A DAG - contains successor information about nodes 
        """
        longest_rank = 0
        for successor in self.graph.successors(node):
#           print successor
            if successor.rank is -1:
                self.rank_up(successor)

            longest_rank = max(longest_rank, self.ave_comm_cost(node,successor)+ successor.rank)

        node.ave_comp = self.ave_comp_cost(node.tid)
        node.rank = node.ave_comp + longest_rank
        node.rank

    def rank_sort_tasks(self):
        """
        Model from this: http://stackoverflow.com/questions/403421/
        how-to-sort-a-list-of-objects-based-on-an-attribute-of-the-objects

        ut.sort(key=lambda x: x.count, reverse=True)

        Sort Tasks by rank provided. According to Topcuolgu et al.(2002), 
        this is a topological order of tasks
        """
        nodes = self.graph.nodes()
        nodes.sort(key=lambda x: x.rank, reverse=True)

        return nodes
    

    def top_sort_tasks(self):
        """
        Use networkx library built-in topological sort function to generate a sorted
        list of tasks based on precedence constraints. This is to test whether or 
        not the ranking heuristic is any better than a topological sort approach
        """
        sort_list=nx.topological_sort(self.graph)
        return sort_list
    
    def calc_est(self,node,processor):
        """
        Calculate the Estimated Start Time of a node on a given processor
        """
        
        est = 0 # If the node does not have predecessors
        predecessors = self.graph.predecessors(node)
        for pretask in predecessors:
            if pretask.processor != processor: # If task isn't on the same processor
                comm_cost = self.comm_matrix[pretask.tid][node.tid]
            else:
                comm_cost = 0 # task is on the same processor, communication cost is 0

            tmp =  self.comp_matrix[node.tid][processor] + comm_cost
            if tmp > est:
                est = tmp

        return est

    def insertion_policy(graph):
        """
        Allocate tasks to processors following the insertion based policy outline 
        in Tocuoglu et al.(2002)
        """
        return -1
    

# if __name__ == '__main__':
  
