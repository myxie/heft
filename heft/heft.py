"""
Functions for static HEFT implementation
"""

import time
import ast

import networkx as nx

from random import randint
from Queue import *
# from pudb import set_trace

def read_matrix(matrix):
    lines = [] 
    with open(matrix) as f:
        next(f)
        for line in f:
            line = ast.literal_eval(line)
            lines.append(line)
    return lines 


"""
Task class for the HEFT algorithm
"""
class Task(object):

    def __init__(self, tid, comp_cost=[]):
        self.tid = int(tid)# task id - this is unique
        self.ave_comp = -1 # average computation cost 
        self.rank = -1 # This is updated during the 'Task Prioritisation' phase 
        self.oct_rank =dict() 
        self.processor = -1
        self.ast = 0 
        self.aft = 0 
        self.comp_cost = comp_cost # List of computation cost on each processor 

    def __repr__(self):
        return str(self.tid)
    """
    To utilise the NetworkX graph library, we need to make the node structure hashable  
    Implementation adapted from: http://stackoverflow.com/a/12076539        
    """

    def __hash__(self):
        return hash(self.tid)

    def __eq__(self, task):
        if isinstance(task, self.__class__):
            return self.tid == task.tid
        return NotImplemented

    """
    Networkx requires an object to be iterable; given comp_cost is a list, 
    we might as well make that the return of the iteration as we can use it
    in the HEFT algorithm
    """
    def __iter__(self):
        return self.comp_cost

class Heft(object):
    def __init__(self, comp, comm, graphml):
        self.graph = nx.read_graphml(graphml,Task)
        self.comp_matrix = read_matrix(comp)
        self.comm_matrix = read_matrix(comm)
        self.processors = dict()
        self.oct_processors = dict()
        num_processors = len(self.comp_matrix[0])
        self.oct_matrix = dict()
        self.oct_rank_matrix = dict()

        keys =  [x for x in range(0,num_processors)]
        #for node in list(list(self.graph.nodes())):
        #    node.oct_rank_dict = {key: -1 for key in keys}
        for x in range(0,num_processors):
            self.processors[x]=[]
            self.oct_processors[x]=[]
         
        self.rank_sort = []
        self.top_sort = []

    def rank(self, method,processor=0):
        if method == 'up':
            for node in sorted(list(self.graph.nodes())):
                self.rank_up(node)
            self.rank_sort = self.rank_sort_tasks()
            self.top_sort = self.top_sort_tasks()

        elif method == 'oct':
            for val in range(0,len(self.processors)):
                for node in sorted(list(self.graph.nodes()),reverse=True): 
                    self.rank_oct(node,val)
            
            for node in list(self.graph.nodes()):
                ave = 0
                for (n, p) in self.oct_rank_matrix:
                    if n is node.tid:
                        ave += self.oct_rank_matrix[(n,p)]

                # if ave_list:         
                node.rank = ave/len(self.processors)
                # else: 
                #     node.rank = sum(ave_list)/1

            self.rank_sort = self.rank_sort_tasks()
            self.top_sort = self.top_sort_tasks()


    def show_rank(self):

        for node in list(self.graph.nodes()):
            print node.rank

    def ave_comm_cost(self,node,successor):
        """
        Returns the 'average' communication cost, which is just 
        the cost in the matrix. Not sure how the ave. in the 
        original paper was calculate or represented...
            
        :params node: Starting node
        :params successor: Node with which the starting node is communicating
        """
        cost = self.comm_matrix[node][successor]
        return cost 

    def ave_comp_cost(self,tid):
        comp = self.comp_matrix[tid]
        return sum(comp)/len(comp)

    def max_comp_cost(self,tid):
        comp = self.comp_matrix[tid]
        return max(comp)

    def min_comp_cost(self, tid):
        comp = self.comp_matrix[tid]
        return min(comp)


    def rank_up(self,node):
        """
        Upward ranking heuristic outlined in Topcuoglu, Hariri & Wu (2002)
        Closely modelled off 'cal_up_rank' function at: 
        https://github.com/oyld/heft/blob/master/src/heft.py

        :param node: A task node in an DAG that is being ranked
        """
        longest_rank = 0
        for successor in self.graph.successors(node):
            if successor.rank is -1:
                self.rank_up(successor)

            longest_rank = max(longest_rank, self.ave_comm_cost(node.tid,successor.tid)+\
                    successor.rank)

        node.ave_comp = self.ave_comp_cost(node.tid)
        node.rank = node.ave_comp + longest_rank

    def rank_up_random(self,node):
        """
        Computes the upward rank based on either the average, max or minimum computational cost
        """

        longest_rank = 0
        for successor in self.graph.successors(node):
            if successor.rank is -1:
                self.rank_up(successor)

            longest_rank = max(longest_rank, self.ave_comm_cost(node.tid,successor.tid)+\
                    successor.rank)

        entropy = randint(0,1000)%3
        if entropy is 0:
            node.ave_comp = self.ave_comp_cost(node.tid)
        elif entropy is 1:
            node.ave_comp = self.max_comp_cost(node.tid)
        elif entropy is 2: 
            node.ave_comp = self.max_comp_cost(node.tid)

        node.rank = node.ave_comp + longest_rank


        return -1

    def rank_oct(self, node, pk):
        """
        Optimistic cost table ranking heuristic outlined in 
        Arabnejad and Barbos (2014)
        """
#       set_trace()
        max_successor = 0
        for successor in self.graph.successors(node):
            min_processor=1000
            for processor in range(0,len(self.processors)):
                oct_val = 0
                if (successor.tid, processor) not in self.oct_rank_matrix.keys():
                    self.rank_oct(successor, processor) 
                comm_cost = 0
                comp_cost = self.comp_matrix[successor.tid][processor] 
                if processor is not pk:
                    comm_cost = self.ave_comm_cost(node.tid, successor.tid)
                oct_val = self.oct_rank_matrix[(successor.tid,processor)] +\
                        comp_cost+ comm_cost
                min_processor = min(min_processor,oct_val)
            max_successor = max(max_successor, min_processor)
        
        self.oct_rank_matrix[(node.tid,pk)] = max_successor

    def rank_stochastic(self, node, pk):
        return -1

        
    
    def rank_sort_tasks(self):
        """ 
        Model from this: http://stackoverflow.com/questions/403421/
        how-to-sort-a-list-of-objects-based-on-an-attribute-of-the-objects

        ut.sort(key=lambda x: x.count, reverse=True)

        Sort Tasks by rank provided. According to Topcuolgu et al.(2002), 
        this is a topological order of tasks
        """
        nodes = list(self.graph.nodes())
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

    def critical_path(self):
        top_sort = self.top_sort_tasks()
        dist = [-1 for x in range(len(list(self.graph.nodes())))]
        dist[0] = 0
        critical_path = []

        for u in top_sort:
            for v in list(self.graph.edges(u)):
                tmp_v = v[1]
                if dist[v[1].tid] < dist[u.tid] + min(self.comp_matrix[v[1].tid])+ self.comm_matrix[v[1].tid][u.tid]:
                    dist[v[1].tid] = dist[u.tid] + min(self.comp_matrix[v[1].tid]) + self.comm_matrix[v[1].tid][u.tid]
                    tmp_v = v[1]

        
        final_dist=dist[len(list(list(self.graph.nodes())))-1]
        critical_path.append(len(list(list(self.graph.nodes())))-1)
        q = Queue()
        q.put(len(list(self.graph.nodes()))-1)


        while not q.empty():
            u = q.get()
            tmp_max = 0
            for v in list(self.graph.predecessors(Task(u))):
                if dist[v.tid] > tmp_max:
                    tmp_max = dist[v.tid]
                    tmp_v=v.tid
                    if tmp_v not in critical_path:
                        critical_path.append(tmp_v)
                    q.put(tmp_v)
                elif dist[v.tid] is 0:
                    tmp_v = 0 # this is the first node in the graph
                    if tmp_v not in critical_path:
                        critical_path.append(tmp_v)
        cp_min = 0
        for x in critical_path:
            cp_min = cp_min + min(self.comp_matrix[x])

        return cp_min

    def sequential_execution(self):
        seq = 1000000
        
        for p in range(len(self.processors)):
            comp = 0 
            for task in list(self.graph.nodes()):
                comp = comp + self.comp_matrix[task.tid][p]
            if comp < seq:
                seq = comp

        return seq
    
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

        # Now we find the time it fits in on the processor
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
    
    def insertion_policy(self,option=None):
        """
        Allocate tasks to processors following the insertion based policy outline 
        in Tocuoglu et al.(2002)
        """
        nodes = list(self.graph.nodes())
        r_sorted = self.rank_sort
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
                # print 'in else'
                aft = 1000000 # a big number
                for processor in range(len(self.processors)):
                    # tasks in r_sorted are being updated, not self.graph; pass in r_sorted
                    est = self.calc_est(task, processor,r_sorted)
                    # print str(task.tid) + ": " + str(est + self.comp_matrix[task.tid][processor])
                    if est + self.comp_matrix[task.tid][processor] < aft:
                        aft = est + self.comp_matrix[task.tid][processor]
                        p = processor
    
                task.processor = p
                task.ast = aft - self.comp_matrix[task.tid][p]
                task.aft = aft
                if task.aft >= makespan:
                   makespan = task.aft
                self.processors[p].append((task.ast, task.aft,str(task.tid)))
                self.processors[p].sort(key=lambda x: x[0])
            # print self.processors

        return makespan


    def insertion_policy_oct(self):
        """
        Allocate tasks to processors following the insertion based policy outline 
        in Tocuoglu et al.(2002)
        """

        nodes = list(self.graph.nodes())
        r_sorted = self.rank_sort
        makespan = 0
        if not self.oct_rank_matrix:
            self.rank('oct')
        eft_matrix = dict()
        oeft_matrix = dict()
        count = 0
        p=0
        for task in r_sorted:
            if task == r_sorted[0]:
                task.ast = 0
                min_oeft = 1000
                for processor in range(len(self.processors)):
                    eft_matrix[(task.tid,processor)] = self.comp_matrix[task.tid][processor]
                    oeft_matrix[(task.tid,processor)]  =  eft_matrix[(task.tid,processor)] + self.oct_rank_matrix[(task.tid,processor)]
                    if oeft_matrix[(task.tid,processor)]  < min_oeft: 
                        min_oeft = oeft_matrix[(task.tid,processor)]
                        p = processor
                task.aft = self.comp_matrix[task.tid][p]
                task.processor = p
                self.processors[p].append((task.ast,task.aft,str(task.tid)))

            else:
                aft = 1000000 # a big number
                min_oeft = 100000
                for processor in range(len(self.processors)):
                    if self.graph.predecessors(task):
                        est = self.calc_est(task,processor,r_sorted)
                    else:
                        est=0
                    eft = est + self.comp_matrix[task.tid][processor]
                    eft_matrix[(task.tid,processor)] =eft
                    oeft_matrix[(task.tid,processor)]  =  eft_matrix[(task.tid,processor)] + self.oct_rank_matrix[(task.tid,processor)]
                    if oeft_matrix[(task.tid,processor)]  < min_oeft: 
                        min_oeft = oeft_matrix[(task.tid,processor)]
                        p = processor
                task.aft =  eft_matrix[(task.tid,p)]  
                task.ast = task.aft - eft_matrix[(task.tid,p)]
                task.processor = p
                if task.aft >= makespan:
                    makespan = task.aft
                self.processors[p].append((task.ast, task.aft,str(task.tid)))
                self.processors[p].sort(key=lambda x: x[0]) 
                count = count + 1

        return makespan

    def greedy_policy(self):
        nodes = list(self.graph.nodes())
        r_sorted = self.rank_sort
        makespan = 0
        for task in r_sorted:
            if task == r_sorted[0]:
                w = min(self.comp_matrix[task.tid])
                p = self.comp_matrix[task.tid].index(w)
                task.processor = p
                task.ast = 0
                task.aft = w
                self.processors[p].append((task.ast, task.aft, str(task.tid)))                
                    
            else:
                est = 0
                tmp_task = None
                for pretask in list(self.graph.predecessors(task)):
                    index = r_sorted.index(pretask)
                    tmp_task = r_sorted[index]
                    aft = r_sorted[index].aft
                    # print "Task {0} has pre-task {1} with aft: {2}".format(task.tid,tmp_task.tid,aft)
                    tmp = aft
                    if tmp >= est:
                        est = tmp
                        tmp_task = pretask

                # print "Pre-task of task {2}with the highest AFT is Task{0}, with aft of {1}".format(tmp_task,est,task)
                # est = 100000
                p = 0 
                allowed_est = est
                est = 1000000
                for processor in self.processors:
                    if len(self.processors[processor]) is not 0:
                        # This sorts the processor by the latest finish time on the processor, which is the earliest available time without searching for slots before
                        # print self.processors[processor][0]
                        self.processors[processor].sort(key=lambda x:x[1],reverse=True)
                        time_slot = self.processors[processor][0]
                        # print time_slot
                        if (time_slot[1] >=allowed_est) and (time_slot[1] <= est): 
                            est = time_slot[1]
                            p = processor

                # print "Est for task {0} is {1}".format(task, est)
                for processor in self.processors:
                    if len(self.processors[processor]) is 0:
                        if est > allowed_est:
                            est = allowed_est
                            p = processor                   


                comm_cost = 0
                if list(self.graph.predecessors(task)):          
                    if tmp_task.processor is not p:
                        comm_cost = self.comm_matrix[tmp_task.tid][task.tid]
                
                w = self.comp_matrix[task.tid][p]
                aft = w + comm_cost + est
                task.aft = aft
                task.ast = aft - w
                if task.aft >= makespan:
                   makespan = task.aft

                self.processors[p].append((task.ast, task.aft,str(task.tid)))
                self.processors[p].sort(key=lambda x: x[1],reverse=True)

        # print self.processors

        return makespan 


    def schedule(self, schedule='insertion'):
        if schedule is 'insertion':
            retval = self.insertion_policy()
        elif schedule is 'oct_schedule':
            retval = self.insertion_policy_oct()
        elif schedule is 'greedy':
            retval = self.greedy_policy()

        return retval

    def display_schedule(self):
        retval = self.insertion_policy() 
        return retval
        

  
