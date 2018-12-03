#!usr/bin
# Python script to bulk-unroll logical graph templates from 
# the DALiuGE data set

# Copyright (C) date RW Bunney

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

import os
import subprocess
"""
Things we need:
    - location (directory) of the LGT
    - find all .json files in that directory (basic sanity check)
    - add them to a list with their absolute path names

"""
print os.listdir('.')
location = '../daliuge/daliuge-logical-graphs/More Edited Pipelines/'

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
