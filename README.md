# Heterogeneous Earliest-Finish-Time

This repository contains source code for an implementation of the HEFT algorithm.

HEFT is organised into 2 phases: 

    * Task Prioritisation
    * Processor Allocation

and runs on a Directed Acyclic Graph (DAG). This project uses the popular NetworkX library for convenience of creating new graphs and leveraging off existing functionality.


## Using the code

Currently, running the code is a WIP, as the class structure in heft/heft.py is a bit of a mess (confusing mess of mutable and immutable class variables). 

tests/tests.py has some examples of how to instantiate a Heft object, which is required in order to schedule a DAG. Other examples can be seen in the analysis folder. 
"""