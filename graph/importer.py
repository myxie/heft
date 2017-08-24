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
     if os.path.exists(path) and (os.stat(path).st_size != 0): 
              
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
        
        nx.topological_sort(G)
        
        variable = 'data/input/graphml/'
#        if os.path.exits(variable):
        title = key.split('.')[0]
        save = variable +title 
        #fname = open('{0}.graphml'.format(save),'w+')
        nx.write_graphml(G, '{0}.graphml'.format(save))

        translate = dict()
        count = 0 

        for node in nx.topological_sort(G):
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

        variable = 'data/input/graphml/translated'
        save = variable+title
        nx.write_graphml(translated_graph, '{0}.graphml'.format(save))


