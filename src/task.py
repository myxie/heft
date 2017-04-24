"""
Task class for the HEFT algorithm
"""

class Task(object):

    def __init__(self, tid, comp_cost=[]):
        self.tid = tid # task id - this is unique
        self.comp_cost = comp_cost # List of computation cost on each processor 
        self.ave_comp = -1 # average computation cost
        self.ave_comm = -1 # average communication cost 
        self.rank = -1 # This is updated during the 'Task Prioritisation' phase 
        self.start = 0 
        self.finish = 0 

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