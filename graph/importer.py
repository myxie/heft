#/usr/bin 
# Script to import a DALiuGE Physical Graph Template (PGT)
import os
import sys
import json
import networkx as nx

location = 'data/input/json/'
graphs = dict() 

for val in os.listdir(location):
    graphs[val]=location
         
for key in graphs:
     path = graphs[key]+key
     print "'Path is:" + path +"'"
     if os.path.exists(path): 
              
        graph = dict()
        with open(path) as f:
            graph = json.load(f)

        G = nx.DiGraph()

        for val in graph:
            G.add_node(val['oid'])

        for val in graph:
            if 'outputs' in val:
                for item in val['outputs']:
                    G.add_edge(val['oid'],item)
            elif 'consumers' in val:
                for item in val['consumers']:
                    G.add_edge(val['oid'],item)

        for node in G.nodes():
            G.node[node]['label']=str(node)
        
        variable = 'data/input/graphml/'
#        if os.path.exits(variable):
        save = variable + key.split('.')[0]
        #fname = open('{0}.graphml'.format(save),'w+')
        nx.write_graphml(G, '{0}.graphml'.format(save))

        translate = dict()
        count = 0 

        for node in G.nodes():
            translate[node] = count 
            count = count+1

        for key, val in translate.items():
            print str(key) + ' :' + str(val) 

        translated_graph = nx.DiGraph()

        for key in translate:
            translated_graph.add_node(translate[key])

        for edge in G.edges():
            translated_graph.add_edge(translate[edge[0]], translate[edge[1]])

        for node in translated_graph.nodes():
            translated_graph.node[node]['label'] = str(node)

        tmp = save.split('_')
        save = tmp[0]+tmp[1]
        nx.write_graphml(translated_graph, '{0}.graphml'.format(save))


