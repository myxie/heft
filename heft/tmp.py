#Temporary file to store functions that were added into heft.py to run experiments

# Copyright (C) 2017,2018  RW Bunney

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.  




def max_comp_cost(self,tid):
    comp = self.comp_matrix[tid]
    return max(comp)

def min_comp_cost(self,tid):
    comp = self.comp_matrix[tid]
    return min(comp)

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



