## DEPRECATED
Please go to http://github.com/myxie/mosws for updated implementation of HEFT and improved testing/experimentation facilities

# Heterogeneous Earliest-Finish-Time


This repository contains source code for the purposes of comparing HEFT-based scheduling heuristics, and the impact workflow graphs have on the resultant makespan.

HEFT is organised into 2 phases: 

* Task Prioritisation
* Processor Allocation

For this project, the following Task Prioritisation Heuristics are implemented: 
* Upward Rank
* Optimistic Cost-Table (OCT) Ranking

The following Processor Allocation strategies are implemented:
* Greedy Allocation
* Insertion Policy
* OCT-Based Insertion Policy

### Prerequisites

To run the HEFT algorithms (found in the heft/ directory), the following external packages are required:
```
NetworkX
```

To run experiments and generate plots, the following packages are required in addition to the above: 
```
matplotlib
numpy
```

To use some of the graph scripts that unroll and partition DALiuGE graphs, you need to install the DALiuGE project, which can be found [here](https://github.com/ICRAR/daliuge), along with how to find example Logical Graph Templates. 

### Installing
HEFT does not require any installation besides ensuring the above dependencies are installed locally on the machine. 

## Running the tests
Run the following command: 
```
python -m unittest tests.tests
```
And all tests should execute.

### Using HEFT

A Heft object (definied in heft/heft.py) constructs a Directed Acyclic Graph from a graphml file, and text files that hold communication and computational cost matrices. A Heft object is constructed as follows: 
```
heft = Heft('tests/topcuoglu_comp.txt',\
            'tests/topcuoglu_comm.txt',\
            'tests/topcuoglu.graphml')
```

Once as a Heft object is constructed, a ranking strategy can be chosen, e.g.
```
retval = heft.rank('up')
```
and a scheduling policy applied to the graph, e.g.
```
makespan = heft.schedule('insertion')
```

