#! /usr/bin/python
from sqlobject import *
import sys,os
import pydot
import sys
import re

sys.path+=['/home/sleon/public_html/bla/']
from db import *

def gentopology():
	regver = re.compile('.*,(\d+)')
	#NodePair.createTable( ifNotExists=True )
	node_pairs = list(NodePair.select())
	nodes = list(Node.select())
	g=pydot.Dot(type='digraph')

	
	for node in nodes:
		matc = regver.match(node.version)
		if matc:
			nversion = matc.group(1)
		else:
			nversion = '0'

		gnode = pydot.Node(node.name,  label='''\
<<FONT POINT-SIZE="10px"><table CELLBORDER="0" border="0"
  CELLPADDING="0"
  CELLSPACING="3"
><tr><td align="left">%s</td>
</tr><tr><td align="left">%s</td></tr>
<tr><td>Ver. %s</td></tr>
</table></FONT>>''' % (node.name,node.location[0:7],nversion ))
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
