"""
Classes for static HEFT implementation
"""


class Task(object):

    def __init__(self, tid, comp_cost=[]):
        self.tid = tid # task id - this is unique
        self.comp_cost = comp_cost # List of computation cost on each processor 
        self.ave_comp = -1 # average computation cost
        self.ave_comm = -1 # average communication cost 
        self.rank = -1 # This is updated furing the 'Task Prioritisation' phase 
        self.start = 0 
        self.finish = 0 

    """
    To utilise the NetworkX graph library, we need to make the node structure hashable	
    Implementation adapted based on discussion here: http://stackoverflow.com/a/12076539		
    """
    def __hash__(self):
        return hash(self.tid)

    def __eq__(self, task):
        if isinstance(task, self.__class__):
            return self.tid == task.tid
        return NotImplemented 


"""
Resource class for 'processing' Task objects
"""

# class Resource(object):



if __name__ == '__main__':

    task = Task(1)	
    task_ = Task(1)
    if task == task_:
        print 'Success'