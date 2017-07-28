"""

Functions for static HEFT implementation
"""
import networkx as nx
import time
import ast


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
        self.oct_rank_dict = dict() 
        self.oct_rank = -1
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
        print nx.is_directed_acyclic_graph(self.graph)
        self.comp_matrix = read_matrix(comp)
        self.comm_matrix = read_matrix(comm)
        self.processors = dict()
        self.top_processors = dict()
        num_processors = len(self.comp_matrix[0])
        self.oct_matrix = dict()

        for x in range(0,num_processors):
            self.processors[x]=[]
            self.top_processors[x]=[]
        print self.processors
         
        self.rank_sort = []
        self.top_sort = []

    def rank(self, method,processor=0):
        if method == 'up':
            for node in sorted(self.graph.nodes()):
                self.rank_up(node)
                print node.rank
            self.rank_sort = self.rank_sort_tasks()
            self.top_sort = self.top_sort_tasks()

        elif method == 'oct':
            #for val in range(0,processor+1):
            for node in sorted(self.graph.nodes()): 
                self.rank_oct(node,processor)

                print node.rank

            for node in self.graph.nodes():
                ave_list = []
                for key in node.oct_rank_dict:
                    ave_list.append(node.oct_rank_dict[key])
                node.rank = sum(ave_list)/len(ave_list)
#            self.rank_sort = self.rank_sort_tasks()
#            self.top_sort = self.top_sort_tasks()

               

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

    def rank_oct(self, node, pk):
        """
        Optimistic cost table ranking heuristic outlined in Arabnejad and Barbos (2014)
        """
        max_successor = 0
        for successor in self.graph.successors(node):
            #print successor
            min_processor = 1000
            if successor.rank is -1:
                for processor in self.processors:
                    oct_val = 0
                    self.rank_oct(successor, processor) 
                    comm_cost = 0
                    if processor is not pk:
                        comm_cost = self.ave_comm_cost(node.tid, successor.tid)
                    oct_val  = successor.oct_rank_dict[processor] + \
                            self.comp_matrix[successor.tid][processor] + comm_cost 
                    min_processor = min(min_processor,oct_val)
            max_successor = max(max_successor, min_processor)

        node.oct_rank_dict[pk] = max_successor

    
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
    
    def insertion_policy(self):
        """
        Allocate tasks to processors following the insertion based policy outline 
        in Tocuoglu et al.(2002)
        """
        start = time.time() 
 
        nodes = self.graph.nodes()
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
                if task.aft >= makespan:
                   makespan = task.aft
                self.processors[p].append((task.ast, task.aft,str(task.tid)))
                self.processors[p].sort(key=lambda x: x[0])

        finish=time.time()
        insertion_time = (finish-start)*1000
        return r_sorted, self.processors, makespan, insertion_time

    def insertion_policy_top(self):
        """
        Allocate tasks to processors following the insertion based policy outline 
        in Tocuoglu et al.(2002)
        """
        t_sorted = self.top_sort
        self.processors = self.top_processors
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
                if task.aft >= makespan:
                   makespan = task.aft
                self.processors[p].append((task.ast, task.aft,str(task.tid)))
                self.processors[p].sort(key=lambda x: x[0])

        return t_sorted, self.processors, makespan


    def makespan(self):
        start = time.time() 
        val =  self.insertion_policy()
        finish=time.time()
        total_time = (finish-start)*1000
        sort = val[0]
        rank = val[2]
        insertion_time = val[3]
        rank_time = total_time-insertion_time
        return rank,total_time,rank_time,insertion_time

    def top_makespan(self):
        start = time.time() 
        val = self.insertion_policy_top()
        finish=time.time()
        total_time = (finish-start)*1000
        sort = val[0]
        top = val[2]
        return top,total_time

    def display_schedule(self):
        retval = self.insertion_policy() 
        r_sorted = retval[0]
        processors = retval[1]
        makespan = retval[2]
        return retval
        

  
