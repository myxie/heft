#/usr/bin 
# Script to import a DALiuGE Physical Graph Template (PGT)

import sys
import json
import networkx as nx

cli = sys.argv
fname = cli[1]

with open(fname) as f: 
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

nx.write_graphml(G, '/tmp/importer.graphml')

translate = dict()
count = 0 

for node in G.nodes():
    translate[node] = count
    count = count+1

translated_graph = nx.DiGraph()

for key in translate:
    translated_graph.add_node(translate[key])

for edge in G.edges():
    translated_graph.add_edge(translate[edge[0]], translate[edge[1]])

for node in translated_graph.nodes():
    translated_graph.node[node]['label'] = str(node)

nx.write_graphml(translated_graph, '/tmp/translated_importer.graphml')


