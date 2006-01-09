from sqlobject import *
from sqlobject.sqlbuilder import *
import sys,os
import datetime
#mport pydot


uri = 'postgres://tiwsted:severe@127.0.0.1/twisted'
#con = connectionForURI(uri)

#sqlhub.processConnection = con
hub = dbconnection.ConnectionHub()

class NodePair(SQLObject):
	_cacheValue = False
	_connection = hub
        node1 = ForeignKey('Node', notNull=True)
        node2 = ForeignKey('Node', notNull=True)

	backoffmax_node1 = StringCol(length=50, default='5000')
	backoffmax_node2 = StringCol(length=50, default='5000')
	backoffcur_node1 = StringCol(length=50, default='0')
	backoffcur_node2 = StringCol(length=50, default='0')
#	nodes = RelatedJoin('Node')
        index = DatabaseIndex('node1','node2', unique=True)

class Node(SQLObject):
	_cacheValue = False
	_connection = hub
	identity = StringCol(length=100, notNull=True)
	lastUpdate = DateTimeCol(notNull=True, default=datetime.datetime.now())
	name = StringCol(length=50, notNull=True, default='dummy')
	version = StringCol(length=50, notNull=True, default='0')
	lastGoodVersion = StringCol(length=50, notNull=True, default='0')

	location = StringCol(length=50, notNull=True,default='0')
	testnet = StringCol(length=10, notNull=True, default='true')
	testnetPort = StringCol(length=10, notNull=True, default='0')
	inserts = StringCol(length=10, notNull=True, default='0')
	requests = StringCol(length=10, notNull=True, default='0')
	transferring_requests = StringCol(length=10, notNull=True, default='0')
	address = StringCol(length=32,notNull=True,default='0.0.0.0:0')

	active=StringCol(length=1,notNull=True,default='N')
#	edges = RelatedJoin('NodePair')
	index = DatabaseIndex('identity',unique=True)
	
	
	#index2 = DatabaseIndex('name',unique=True)

def init():
	con = get_con()

	Node.createTable(connection=con)
	NodePair.createTable(connection=con)

def drop():
	con = get_con()

	NodePair.dropTable(connection=con)

	Node.dropTable(connection=con)
	
def reinit():
	con = get_con()	
	drop()
	init()

def get_con():
	hub.threadConnection = connectionForURI(uri)
	
	return hub.getConnection()

def getLastGoodVer(trans):
	return trans.queryOne('SELECT MAX(last_good_version) from node')[0]


def delete_conns(nodeinfo, trans):
	nodeid = getIdFromInfo(nodeinfo,trans)
	node = Node.get(nodeid, connection=trans)
	edges = node.edges	

	for edge in edges:
		node1=edge.node1
		node2=edge.node2
		#node1.removeNodePair(edge)
		#node2.removeNodePair(edge)
		edge.delete(edge.id)

def exists(nodeinfo,trans):
	result = Node.select(Node.q.identity == nodeinfo['identity'],connection=trans)

	if list(result):
		return True
	else:
		return False

def number_edges(node):
	return len(list(node.edges))

def refresh(nodeinfo,trans):
	if exists(nodeinfo,trans):
		n = Node.select(Node.q.identity == nodeinfo['identity'],connection=trans)[0]

	else:
		n = Node(identity=nodeinfo['identity'],connection=trans)
	
	for key in nodeinfo.keys():
		setattr(n, key, nodeinfo[key])

	n.lastUpdate = datetime.datetime.now()


def getIdFromInfo(nodeinfo, trans):
	n = Node.select(Node.q.identity == nodeinfo['identity'],connection=trans )
	if list(n):
		return list(n)[0].id
	else:
		raise Exception('No such node!')
	
def insert(trans,nodeinfo1, nodeinfo2, backoff1={}, backoff2={}):

        #NodePair.createTable( ifNotExists=True)
	node1 = getIdFromInfo(nodeinfo1,trans)
	node2 = getIdFromInfo(nodeinfo2,trans)
                        #sorting
        if node1 > node2:
		temp=node2
		node2=node1
		node1=temp

		btemp=backoff2
		backoff2=backoff1
		backoff1=btemp


	bla = NodePair( node1=node1, node2=node2,connection=trans )
	#Node.get(node1, connection=trans).addNodePair(bla)
	#Node.get(node2, connection=trans).addNodePair(bla)
	if backoff1:
		bla.backoffmax_node1 = backoff1['backoffmax']
		bla.backoffcur_node1 = backoff1['backoffcur']

	if backoff2:
		bla.backoffmax_node2 = backoff2['backoffmax']
		bla.backoffcur_node2 = backoff2['backoffcur']

