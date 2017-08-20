"""
An ugly file with miscelaneous functions
"""
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
