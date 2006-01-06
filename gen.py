#! /usr/bin/python
from sqlobject import *
import sys,os
import pydot
import sys

sys.path+=['/home/sleon/public_html/bla/']
from db import *

def gentopology():

	#NodePair.createTable( ifNotExists=True )
	node_pairs = list(NodePair.select())
	nodes = list(Node.select())
	g=pydot.Dot(type='digraph')

	
	for node in nodes:
		gnode = pydot.Node(node.name,  label='''\
<<table CELLBORDER="0" border="0"
  CELLPADDING="0"
  CELLSPACING="0"
><tr><td>%s</td>
</tr><tr><td>%s</td></tr>
</table>>''' % (node.name,node.location) )
		g.add_node(gnode)
	
	#there are no dublicate edges in the database 
	for node_pair in node_pairs:
		gedge = pydot.Edge(node_pair.node1.name, node_pair.node2.name, arrowhead='none')
		g.add_edge(gedge)


	g.write_png('/home/sleon/public_html/output2.png',prog='dot')
#	g.write_dot('bla.dot')

#	return """\
#	<html>
#	<head>
#	<title>Topology of testnetwork(s):</title>
#	<META HTTP-EQUIV="REFRESH" CONTENT="180;URL=http://sleon.dyndns.org/~sleon/functions.py/gentopology">
#	</head>
#	<body>
#	<img alt="topologymap" src=/~sleon/output.png>
#	</body>
#	</html>
#	"""

gentopology()
