#! /usr/bin/python
from sqlobject import *
import sys,os
import pydot
import sys
import re

sys.path+=['/home/sleon/public_html/bla/']
from db import *

regver = re.compile('.*,(\d+)')
	
#COLORS
nodeOK='#9dfbb9'
nodeOUTDATED='#f3fb9d'
edgeOK='#238500'
edgeBLOCKED='#ee4a1e'


def gentopology():
	#NodePair.createTable( ifNotExists=True )
	node_pairs = list(NodePair.select())
	nodes = list(Node.select())
	g=pydot.Dot(type='digraph')
	lastver = regver.match( getLastVer()).group(1)

	
	for node in nodes:

		nodecolor=nodeOK

		matc = regver.match(node.version)
		if matc:
			nversion = matc.group(1)
		else:
			nversion = '0'

		
		if nversion < lastver:
			nodecolor=nodeOUTDATED

		gnode = pydot.Node(node.name, shape='plaintext', label='''\
<<FONT POINT-SIZE="10px"><table bgcolor="%s" CELLBORDER="0" border="1"
  CELLPADDING="2"
  CELLSPACING="3"
><tr><td align="left">%s</td>
</tr><tr><td align="left">%s</td></tr>
<tr><td align="left">Ver. %s</td></tr>
</table></FONT>>''' % (nodecolor, node.name,node.location[0:7],nversion ))
		g.add_node(gnode)
	
	#there are no dublicate edges in the database 
	for node_pair in node_pairs:
		edgecolor = edgeOK


		if node_pair.backoffcur_node1 != '0' or node_pair.backoffcur_node2 != '0':
			edgecolor= edgeBLOCKED
		gedge = pydot.Edge(node_pair.node1.name, node_pair.node2.name, color=edgecolor , arrowhead='none')
		g.add_edge(gedge)


	g.write_png('/tmp/output.png',prog='dot')
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
