# Generates cost matrices based on given number of nodes and processors

# Copyright (C) 2017 RW Bunney

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

from graph import random_comp_matrix, random_comm_matrix

nodes = 1000;
processors = 5;

# generates comp matrices

# for y in range(1001,5000): 
# for x in range(1,processors+1):
# 	random_comp_matrix(x, 1615,15) 
# random_comm_matrix(1615,50)	

# for x in range(1,processors+1):
# 	random_comp_matrix(x, 4583,15) 
# random_comm_matrix(4583,50)	

for x in range(1,processors+1):
	random_comp_matrix(x, 2899,15) 
random_comm_matrix(2899,50)	



# 771, 108,1202,135,3,19603,3467,1095,7719,12498,3271,29227,2899,1615,4583,2068