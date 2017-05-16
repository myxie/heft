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
        self.top_processors = processors # for topological sort comparison
        #print self.graph.nodes()[0].comp_cost        
        self.rank_up(self.graph.nodes()[0])
        self.rank_sort = self.rank_sort_tasks()
        self.top_sort = self.top_sort_tasks()
        #print 'top_sort ' + str(self.top_sort)
        for node in self.graph.nodes():
            print 'node ' + str(node.tid) + 'rank ' + str(node.rank)
        print 'rank_sort ' + str(self.rank_sort)

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
        print nodes

        return nodes
    

    def top_sort_tasks(self):
        """
        Use networkx library built-in topological sort function to generate a sorted
        list of tasks based on precedence constraints. This is to test whether or 
        not the ranking heuristic is any better than a topological sort approach
        """
        sort_list=nx.topological_sort(self.graph)
        return sort_list
    
    def calc_est(self,node,processor_num,task_list):
        """
        Calculate the Estimated Start Time of a node on a given processor
        """
        
        est = 0 # If the node does not have predecessors
        predecessors = self.graph.predecessors(node)
        for pretask in predecessors:
            if pretask.processor != processor_num: # If task isn't on the same processor
                comm_cost = self.comm_matrix[pretask.tid][node.tid]
            else:
                comm_cost = 0 # task is on the same processor, communication cost is 0

            # self.graph.predecessors is not being updated in insertion_policy;
            # need to use the tasks that are being updated to get the right results
            index = task_list.index(pretask)
            aft = task_list[index].aft
            tmp = aft  + comm_cost
            if tmp >= est:
                est = tmp

        processor = self.processors[processor_num] # return the list of allocated tasks
        available_slots = []
        if len(processor) == 0:
            return est # Nothing in the time slots yet, so the earliest start time is whenever
        else:
            for x in range(len(processor)):
                # For each start/finish time tuple that exists in the processor
                if x == 0:
                    if processor[0][0] != 0: #If the start time of the first tuple is not 0
                        available_slots.append((0,processor[0][0]))# add a 0-current_start time tuple
                    else:
                        continue
                else: 
                    # Append the finish time of the previous slot and the start time of this slot
                    available_slots.append((processor[x-1][1],processor[x][0]))
            
            # Add a very large number to the final time slot available, so we have a gap after 
            available_slots.append((processor[len(processor)-1][1],10000))

        for avail in available_slots:
            if est < avail[0] and avail[0]+ self.comp_matrix[node.tid][processor_num] <= avail[1]:
                return avail[0]
            if est >= avail[0] and est + self.comp_matrix[node.tid][processor_num] <= avail[1]:
               return est 

        return est
    
    def insertion_policy(self):
        """
        Allocate tasks to processors following the insertion based policy outline 
        in Tocuoglu et al.(2002)
        """
        nodes = self.graph.nodes()
        r_sorted = self.rank_sort
        print 'r_sorted ' + str(r_sorted)
        makespan = 0
        for task in r_sorted:
            if task == r_sorted[0]:
                w = min(self.comp_matrix[task.tid])
                p = self.comp_matrix[task.tid].index(w)
                task.processor = p
                task.ast = 0
                task.aft = w
                self.processors[p].append((task.ast,task.aft,str(task.tid)))
            else:
                aft = 10000 # a big number
                for processor in range(len(self.processors)):
                    # tasks in r_sorted are being updated, not self.graph; pass in r_sorted
                    est = self.calc_est(task, processor,r_sorted)
                    if est + self.comp_matrix[task.tid][processor] < aft:
                        aft = est + self.comp_matrix[task.tid][processor]
                        p = processor
    
                task.processor = p
                task.ast = aft - self.comp_matrix[task.tid][p]
                task.aft = aft
                #print 'aft: ' + str(task.aft)
                if task.aft >= makespan:
                   makespan = task.aft
                self.processors[p].append((task.ast, task.aft,str(task.tid)))
                self.processors[p].sort(key=lambda x: x[0])

        return r_sorted, self.processors, makespan

    def insertion_policy_top(self):
        """
        Allocate tasks to processors following the insertion based policy outline 
        in Tocuoglu et al.(2002)
        """
        nodes = self.graph.nodes()
        t_sorted = self.top_sort
        print 't_sorted ' + str(t_sorted)
        makespan = 0
        for task in t_sorted:
            if task == t_sorted[0]:
                w = min(self.comp_matrix[task.tid])
                p = self.comp_matrix[task.tid].index(w)
                task.processor = p
                task.ast = 0
                task.aft = w
                self.processors[p].append((task.ast,task.aft,str(task.tid)))
            else:
                aft = 10000 # a big number
                for processor in range(len(self.processors)):
                    # tasks in r_sorted are being updated, not self.graph; pass in r_sorted
                    est = self.calc_est(task, processor,t_sorted)
                    if est + self.comp_matrix[task.tid][processor] < aft:
                        aft = est + self.comp_matrix[task.tid][processor]
                        p = processor
    
                task.processor = p
                task.ast = aft - self.comp_matrix[task.tid][p]
                task.aft = aft
                #print 'aft: ' + str(task.aft)
                if task.aft >= makespan:
                   makespan = task.aft
                self.processors[p].append((task.ast, task.aft,str(task.tid)))
                self.processors[p].sort(key=lambda x: x[0])

        return t_sorted, self.processors, makespan



    def makespan(self):
       
        val =  self.insertion_policy()
        sort = val[0]
        #print 'rank '+str(sort)
        rank = val[2]
        return rank

    def top_makespan(self):
        val = self.insertion_policy_top()
        sort = [0]
        #print 'top ' + str(sort)
        top = val[2]
        return top
           
    def display_schedule(self):
        retval = self.insertion_policy() 
        r_sorted = retval[0]
        processors = retval[1]
        makespan = retval[2]
        return retval
        
    

# if __name__ == '__main__':
  
