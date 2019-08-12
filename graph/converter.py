# Copyright (C) 2019 RW Bunney

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


"""
Module to convert from a graphml DAG to the format required for our MiniZinc model


A ".dzn" file will have the format:

	num_tasks = # e.g. 5
	num_machines = # e.g. 3

	comp_cost = [ # assume '3' machines
				|0,0,0, # Must pad with zeros at beginning and end for 'source' and 'sink'
				|,,,
				|,,,|]

	comm_cost = [# pad each row with 0 at the beginning and end \
				|0,0,0,0,0,0,0,
									(these represent the 'source' and sink nodes')

"""

import networkx
import numpy as np


def convert_from_graphml(graphml):
	self.graph = nx.read_graphml(graphml, int)
	pass


def convert_from_nxobject(nxgraph):
	cost_matrix = np.empty(nxobject.size+2,nxobject.size+2)
	for node in nxgraph.node:
		cost_matrix[node, node] = node

	pass
