#!usr/bin
# Python script to bulk-unroll logical graph templates from 
# the DALiuGE data set
import os
import subprocess
"""
Things we need:
    - location (directory) of the LGT
    - find all .json files in that directory (basic sanity check)
    - add them to a list with their absolute path names

"""
print os.listdir('.')
location = '../daliuge/daliuge-logical-graphs/SDP Pipelines/'

graphs = dict() 
for graph in os.listdir(location):
    graphs[graph]=location

for graph in graphs:
    path = graphs[graph]+graph
    if os.path.exists(path): 
        print path
        cmd_list = ['dlg', 'unroll-and-partition', '-L',path ]
        #f = open('data/input/json/_{0}_unroll.json'.format(graph),'w+') 
        with open('data/input/json/_{0}'.format(graph),'w+') as f:
            subprocess.call(cmd_list,stdout=f)
    else:
        print "Failure to find path {0}".format(graphs[graph]+graph)
