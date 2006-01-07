#! /usr/bin/python
#from sqlobject import *
import sys,os
import pydot
import sys
sys.path+=['/home/sleon/freeviz/']
import re
import handler
import math
import time
import histogram

import db
import sqlobject

	


class Generator(object):



	regver = re.compile('.*,(\d+)')
	#COLORS
	nodeOK='#9dfbb9'
	nodeOUTDATED='#f3fb9d'
	edgeOK='#238500'
	edgeBLOCKED='#ee4a1e'
	defaultSize='8px'
	
	#saves previous state of nodes
	oldnstate={}

	def __init__(self,oldnstate):
		self.oldnstate = oldnstate
	
	#returns identyt location dictionaries list for all ndoes
	def getnstate(self,nodes):
		nstate={}
	
		for node in nodes:
			nstate[node.identity] = (node.location, node.name)
	
		return nstate

	def compute_distance(self, loc1, loc2):
                a = loc1
		b = loc2
                #a number between 0 and 0.5
                delta = min(abs(a-b), 1-abs(a-b))

		return delta
                #index=0
                #chunk=0.5 / float(histogram.precision)
                #for i in range(histogram.precision):
                #        if chunk * float(i) <= delta and chunk * float(i+1) > delta:
                #                index = i
                #                break
		#return index * chunk
	
	def find_and_addswapedge(self, g, nodes, identity, nstate):
		
		oldidentities=[]
		
		for okey in self.oldnstate.keys():
			if oldstate[okey][0] == oldlocation:
				oldidentities.append(okey)
	
		#not eindeutig!!
		if len(oldidentities) != 1 :
			print("name not eindeutig!")	
	
		oldidentity = oldidentities[0]
		print "showing edge between %s and %s" % ( nstate[identity][1], nstate[oldidentity][1])
		gedge=pydot.Gedge(nstate[identity][1], nstate[oldidentity][1], label='swap', taillabel='nstate[identity][0]'
					, headlabel='nstate[oldidentity][0]', arrowtail='vee', arrowhead='vee'  )
	
		g.add_ege(gedge)
	
		
	
	def gentopology(self):
		#NodePair.createTable( ifNotExists=True )
		node_pairs = list(db.NodePair.select())
		assert node_pairs
		nodes = list( handler.get_activenodes())
		assert nodes
		nstate = self.getnstate(nodes)
		assert nstate

		g=pydot.Dot(type='digraph')
		lastver = self.regver.match( db.getLastVer()).group(1)
	
		
		for node in nodes:
	
			nodecolor=self.nodeOK
			transinfosize=self.defaultSize
	
			matc = self.regver.match(node.version)
			if matc:
				nversion = matc.group(1)
			else:
				nversion = '0'
	
			
			if nversion < lastver:
				nodecolor=self.nodeOUTDATED
	
			if node.requests != '0' or node.inserts != '0' or node.transferring_requests != '0':
				transinfosize="10px"
	
			gnode = pydot.Node(node.name, style='filled', color=nodecolor , label='''\
<
	<table CELLBORDER="0" border="0"
	  CELLPADDING="2"
	  CELLSPACING="3">
	<tr><td align="left"><FONT point-size="%s">%s</FONT></td>
	</tr>
	<tr><td align="left"><FONT point-size="%s">%s</FONT></td></tr>
	<tr><td align="left"><FONT point-size="%s">R:%s I:%s TR:%s</FONT></td></tr>
	<tr><td align="left"><FONT point-size="5px">Ver. %s</FONT></td></tr>
	
	</table>
	>''' % (transinfosize, node.name,transinfosize, 
		node.location[0:7], transinfosize, node.requests, 
		node.inserts, node.transferring_requests,nversion))
			g.add_node(gnode)
		
		#there are no dublicate edges in the database 
		for node_pair in node_pairs:
			edgecolor = self.edgeOK
	
			node1loc = float(node_pair.node1.location)
			node2loc = float(node_pair.node2.location)
			distance = self.compute_distance(node1loc, node2loc)
	
			if node_pair.backoffcur_node1 != '0' or node_pair.backoffcur_node2 != '0':
				edgecolor= self.edgeBLOCKED
			gedge = pydot.Edge(node_pair.node1.name , node_pair.node2.name, color=edgecolor , fontcolor=edgecolor,
							label='d: %f' % distance, fontsize='9.5',arrowhead='none')
			#node1 is tail, node2 is head
			if edgecolor == self.edgeBLOCKED:
				if node_pair.backoffcur_node1 != '0':
					gedge.taillabel='%s (%s)' % (node_pair.backoffmax_node1, node_pair.backoffcur_node1 ) 
					gedge.arrowtail='tee'
				if node_pair.backoffcur_node2 != '0':
					gedge.headlabel='%s (%s)' % (node_pair.backoffmax_node2, node_pair.backoffcur_node2 ) 
					gedge.arrowhead='tee'
	
	
			g.add_edge(gedge)
	
			
		if self.oldnstate:
			for identity in nstate.keys():
				if identity in self.oldnstate:
					if self.oldnstate[identity] != nstate[identity]:
						print('location swap detected')
						self.find_and_addswapedge(g, nodes, identity, nstate) 
		else:
			print "oldnstate empty!"
	
		g.write_png('/tmp/output.png',prog='dot')
	
		self.oldnstate = nstate
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

oldnstate={}
while(True):
	generator = Generator(oldnstate)
	generator.gentopology()
	histogram.gen()
	oldnstate = generator.oldnstate
	del generator
	del histogram
	
	del db
	time.sleep(100)
	print "iter"

	import histogram
	import db

