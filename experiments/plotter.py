#An ugly file with miscelaneous functions

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


from graph import random_dag
import matplotlib.pyplot as plt
import time

def run_random_dag():

    time_list = [] 
    n_list = [x for x in range(10,1001, 10)]
    for n in range (10, 1001, 10):
        start = time.time()
        g = random_dag(n,n)
        finish = time.time()
        time_list.append((finish-start)*1000)

    plt.plot(n_list, time_list)
    plt.show()
