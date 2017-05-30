"""
Functions for static HEFT implementation
"""
import networkx as nx
import task 
import time
from graph import create_processors
import copy


class Heft(object):
    def __init__(self, graph, comm, comp,num_processors):
        tmp = graph
        self.graph = graph
        self.max_graph =copy.deepcopy(graph) 
        self.min_graph = copy.deepcopy(graph)
        self.comm_matrix = comm
        self.comp_matrix = comp
        self.processors = create_processors(num_processors) 
        self.top_processors = create_processors(num_processors) # for topological sort comparison
        self.max_processors = create_processors(num_processors)
        self.min_processors = create_processors(num_processors)
        #print self.graph.nodes()[0].comp_cost        
        #nodeA = self.graph.nodes()[0]
        # for node in self.graph.nodes():
            # print node.rank
        for node in self.graph.nodes():
            self.rank_up(node)

        self.rank_sort = self.rank_sort_tasks()
        # print self.rank_sort

        # for node in self.max_graph.nodes():
            # print node.rank
        for node in self.max_graph.nodes():
            self.rank_up_max(node)
        self.max_rank_sort = self.max_graph.nodes() 
        self.max_rank_sort.sort(key=lambda x: x.rank, reverse=True)
        # print self.max_rank_sort

        for node in self.min_graph.nodes():
            self.rank_up_min(node)
        self.min_rank_sort = self.min_graph.nodes()
        self.min_rank_sort.sort(key=lambda x: x.rank, reverse=True)
        # print self.max_rank_sort
        # print self.min_rank_sort
        # tasks = tasks_orig
        # for node in tasks:
        #     self.rank_up_comp(node)

        self.top_sort = self.top_sort_tasks()
        #print 'top_sort ' + str(self.top_sort)
        #for node in self.graph.nodes():
        #    print 'node ' + str(node.tid) + 'rank ' + str(node.rank)
        #print 'rank_sort ' + str(self.rank_sort)

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

    def max_comp_cost(self,tid):
        comp = self.comp_matrix[tid]
        return max(comp)

    def min_comp_cost(self,tid):
        comp = self.comp_matrix[tid]
        return min(comp)

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
            if successor.rank is -1:
                self.rank_up(successor)

            longest_rank = max(longest_rank, self.ave_comm_cost(node,successor)+ successor.rank)

        node.ave_comp = self.ave_comp_cost(node.tid)
        node.rank = node.ave_comp + longest_rank

    def rank_up_max(self,node):
        """
        Upward ranking heuristic outlined in Topcuoglu, Hariri & Wu (2002)
        Closely modelled off 'cal_up_rank' function at: 
        https://github.com/oyld/heft/blob/master/src/heft.py

        :param node: A task node in an DAG that is being ranked
        :param graph: A DAG - contains successor information about nodes 
        """
        longest_rank = 0
        for successor in self.max_graph.successors(node):
            if successor.rank is -1:
                self.rank_up_max(successor)

            longest_rank = max(longest_rank, self.ave_comm_cost(node,successor)+ successor.rank)

        node.ave_comp = self.max_comp_cost(node.tid)
        node.rank = node.ave_comp + longest_rank

    def rank_up_min(self,node):
        """
        Upward ranking heuristic outlined in Topcuoglu, Hariri & Wu (2002)
        Closely modelled off 'cal_up_rank' function at: 
        https://github.com/oyld/heft/blob/master/src/heft.py

        :param node: A task node in an DAG that is being ranked
        :param graph: A DAG - contains successor information about nodes 
        """
        longest_rank = 0
        for successor in self.min_graph.successors(node):
            if successor.rank is -1:
                self.rank_up_min(successor)

            longest_rank = max(longest_rank, self.ave_comm_cost(node,successor)+ successor.rank)

        node.ave_comp = self.min_comp_cost(node.tid)
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
        #print nodes

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
        # print self.processors
        #print 'r_sorted ' + str(r_sorted)
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

        finish=time.time()
        insertion_time = (finish-start)*1000
        print self.processors
        return r_sorted, self.processors, makespan, insertion_time

    def insertion_policy_top(self):
        """
        Allocate tasks to processors following the insertion based policy outline 
        in Tocuoglu et al.(2002)
        """
        t_sorted = self.top_sort
#       print 't_sorted ' + str(t_sorted)
        # tmp = self.empty_processors #reset processors
        self.processors = self.top_processors
        # print self.processors
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

        print self.processors
        return t_sorted, self.processors, makespan

    def insertion_policy_max(self):
        """
        Allocate tasks to processors following the insertion based policy outline 
        in Tocuoglu et al.(2002)
        """
        t_sorted = self.max_rank_sort
#       print 't_sorted ' + str(t_sorted)
        # tmp = self.empty_processors #reset processors
        self.processors = self.max_processors
        # # print self.processors
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

    def insertion_policy_min(self):
        """
        Allocate tasks to processors following the insertion based policy outline 
        in Tocuoglu et al.(2002)
        """
        t_sorted = self.min_rank_sort
#       print 't_sorted ' + str(t_sorted)
        # tmp = self.empty_processors #reset processors
        self.processors = self.min_processors
        # print self.processors
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
        start = time.time() 
        val =  self.insertion_policy()
        finish=time.time()
        total_time = (finish-start)*1000
        sort = val[0]
        #print 'rank '+str(sort)
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
        #print 'top ' + str(sort)
        top = val[2]
        return top,total_time

    def max_makespan(self):
        start = time.time() 
        val = self.insertion_policy_max()
        finish=time.time()
        total_time = (finish-start)*1000
        sort = val[0]
        #print 'top ' + str(sort)
        top = val[2]
        return top,total_time

    def min_makespan(self):
        start = time.time() 
        val = self.insertion_policy_min()
        finish=time.time()
        total_time = (finish-start)*1000
        sort = val[0]
        #print 'top ' + str(sort)
        top = val[2]
        return top,total_time



    def display_schedule(self):
        retval = self.insertion_policy() 
        r_sorted = retval[0]
        processors = retval[1]
        makespan = retval[2]
        return retval
        
    

# if __name__ == '__main__':
  
