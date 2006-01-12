#! /usr/bin/python
#from sqlobject import *
import sys,os
import pydot
import sys
sys.path+=['/home/sleon/freeviz/']
import re
import handler
import math
from time import sleep
import histogram
import ciclegraph

import db
from datetime import *

	


class Generator(object):



	regver = re.compile('.*,(\d+)')
	#COLORS
	nodeOK='#9dfbb9'
	nodeOUTDATED='#c5ffff'
	#nodeOUTDATED='#f9ffcb'
#	nodeLCONNS=nodeOK

	edgeOK='#238500'
	edgeBLOCKED='#ee4a1e'
	edgeCRITICAL='#c08000'
	defaultSize='3px'
#	minEdges=3
	
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
			if oldnstate[okey][0] == nstate[identity][0]:
				oldidentities.append(okey)
	
		#not eindeutig!!
		if len(oldidentities) != 1 :
			print("name not eindeutig!")	
			return
	
		oldidentity = oldidentities[0]
		#print "showing edge between %s and %s" % ( nstate[identity][1], nstate[oldidentity][1])
		#emergency
		if not(identity in nstate and oldidentity in nstate):
			return
		gedge=pydot.Edge(nstate[identity][1], nstate[oldidentity][1], label='swap', 
					taillabel='%s' % nstate[identity][0],
					headlabel='%s' %nstate[oldidentity][0], arrowtail='vee', arrowhead='vee'  )
	
		g.add_edge(gedge)
	
	def gentopology(self,trans):
		#NodePair.createTable( ifNotExists=True )
		node_pairs = list(db.NodePair.select(connection=trans))
		if not node_pairs:
			print "node_pairs is empty"
		nodes = list( handler.get_activenodes(trans))
		if not nodes:
			print "got empty active nodes list!"

		#number of edges and nodes in grapgh
		nnum=len(nodes)
		enum=len(node_pairs)

		nstate = self.getnstate(nodes)
		if not nstate:
			print "got empty nstate list"

		g=pydot.Dot(type='digraph', labelloc='tl', label='Nodes: %s, Edges: %s, Time: %s' % (nnum, enum, datetime.now())  )
		lastgoodver = db.getLastGoodVer(trans)
	
		#counts edges for a node	
		#edge_count={}
	
		for node in nodes:
			#edge_count[node.name]=0
			nodecolor=self.nodeOK
			transinfosize=self.defaultSize
	

			nversion = self.regver.match(node.version).group(1)
			if node.lastGoodVersion < lastgoodver:
				nodecolor=self.nodeOUTDATED
		#	elif db.number_edges(node) < self.minEdges:
		#		nodecolor=self.nodeLCONNS
	
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
			#assert node_pair.node1.name in edge_count
			#edge_count[node_pair.node1.name]+=1

			#assert node_pair.node2.name in edge_count
			#edge_count[node_pair.node2.name]+=1

			edgecolor = self.edgeOK
	
			node1loc = float(node_pair.node1.location)
			node2loc = float(node_pair.node2.location)
			distance = self.compute_distance(node1loc, node2loc)
	
			if node_pair.backoffcur_node1 != '0' or node_pair.backoffcur_node2 != '0':
				edgecolor= self.edgeBLOCKED
			elif node_pair.backoffmax_node1 != '5000' or node_pair.backoffmax_node2 != '5000':
				edgecolor= self.edgeCRITICAL
			#print "adding %s-%s" % (node_pair.node1.name,node_pair.node2.name)
			gedge = pydot.Edge(node_pair.node1.name , node_pair.node2.name, color=edgecolor , fontcolor=edgecolor, 
							label='d: %0.3f' % distance, fontsize='9.5',arrowhead='none')
			#node1 is tail, node2 is head
			if edgecolor == self.edgeBLOCKED:
				if node_pair.backoffcur_node1 != '0':
					gedge.taillabel='%s (%s)' % (node_pair.backoffmax_node1, node_pair.backoffcur_node1 ) 
					gedge.arrowtail='tee'
				if node_pair.backoffcur_node2 != '0':
					gedge.headlabel='%s (%s)' % (node_pair.backoffmax_node2, node_pair.backoffcur_node2 ) 
					gedge.arrowhead='tee'
			elif edgecolor == self.edgeCRITICAL:
				if node_pair.backoffmax_node1 != '5000':
					gedge.taillabel='%s' % (node_pair.backoffmax_node1)
				if node_pair.backoffmax_node2 != '5000':
					gedge.headlabel='%s' % (node_pair.backoffmax_node2)

	
			g.add_edge(gedge)
	

#		for node_name in edge_count.keys():
#			if edge_count[node_name] < self.minEdges:
#				if g.get_node(node_name).color != self.nodeOUTDATED:
#					g.get_node(node_name).color=self.nodeLCONNS

			
		if self.oldnstate:
			for identity in nstate.keys():
				if identity in self.oldnstate:
					if self.oldnstate[identity] != nstate[identity]:
						print('\nLOCATION SWAP  detected!!!!!!!!!!!!!!!!!!!!!!\n')
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
if len(sys.argv) > 1:
	delay=int(sys.argv[1])
else:
	delay=60

print "delay is %d" % delay
while(True):
	con = db.get_con()
	trans = con.transaction()
	generator = Generator(oldnstate)
	#STARING TRANS
	generator.gentopology(trans)
	histogram.gen(trans)
	ciclegraph.gen(trans)
	#COMMITING TRANS
	trans.commit()
	oldnstate = generator.oldnstate
	trans.close()
	db.close_con(con)
	sleep(delay)
