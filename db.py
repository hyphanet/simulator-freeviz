from sqlobject import *
from sqlobject.sqlbuilder import *
import sys,os
import datetime
#mport pydot


uri = 'mysql://twisted:severe@127.0.0.1/twisted?cache=False'
con = connectionForURI(uri)
sqlhub.processConnection = con

class NodePair(SQLObject):
        node1 = ForeignKey('Node', notNull=True)
        node2 = ForeignKey('Node', notNull=True)

	backoffmax_node1 = StringCol(length=50, default='5000')
	backoffmax_node2 = StringCol(length=50, default='5000')
	backoffcur_node1 = StringCol(length=50, default='0')
	backoffcur_node2 = StringCol(length=50, default='0')
        index = DatabaseIndex('node1','node2', unique=True)

class Node(SQLObject):
	identity = StringCol(length=100, notNull=True)
	lastUpdate = DateTimeCol(notNull=True, default=datetime.datetime.now())
	name = StringCol(length=50, notNull=True, default='dummy')
	version = StringCol(length=50, notNull=True, default='0')

	location = StringCol(length=50, notNull=True,default='0')
	testnet = StringCol(length=10, notNull=True, default='true')
	testnetPort = StringCol(length=10, notNull=True, default='0')
	inserts = StringCol(length=10, notNull=True, default='0')
	requests = StringCol(length=10, notNull=True, default='0')
	transferring_requests = StringCol(length=10, notNull=True, default='0')
	address = StringCol(length=32,notNull=True,default='0.0.0.0:0')

	index = DatabaseIndex('identity',unique=True)
	#index2 = DatabaseIndex('name',unique=True)

def getLastVer():
	return con.queryOne('SELECT MAX(version) from node')[0]

def init():
	Node.createTable()
	NodePair.createTable()

def drop():
	Node.dropTable()
	NodePair.dropTable()

def reinit():
	drop()
	init()

def delete_conns(nodeinfo):
	nodeid = getIdFromInfo(nodeinfo)
	l = NodePair.select()
	for i in l:
		if i.node1.id == nodeid or i.node2.id == nodeid:
			i.delete(i.id)

def exists(nodeinfo):
	result = Node.select(Node.q.identity == nodeinfo['identity'])

	if list(result):
		return True
	else:
		return False


def refresh(nodeinfo):
	if exists(nodeinfo):
		n = Node.select(Node.q.identity == nodeinfo['identity'])[0]

	else:
		n = Node(identity=nodeinfo['identity'])
	
	for key in nodeinfo.keys():
		setattr(n, key, nodeinfo[key])

	n.lastUpdate = datetime.datetime.now()


def getIdFromInfo(nodeinfo):
	n = Node.select(Node.q.identity == nodeinfo['identity'] )
	if list(n):
		return list(n)[0].id
	else:
		raise Exception('No such node!')
	
def insert(nodeinfo1, nodeinfo2, backoff1={}, backoff2={}):

        #NodePair.createTable( ifNotExists=True)
	node1 = getIdFromInfo(nodeinfo1)
	node2 = getIdFromInfo(nodeinfo2)
                        #sorting
        if node1 > node2:
		temp=node2
		node2=node1
		node1=temp

		btemp=backoff2
		backoff2=backoff1
		backoff1=btemp


	bla = NodePair( node1=node1, node2=node2 )
	if backoff1:
		bla.backoffmax_node1 = backoff1['backoffmax']
		bla.backoffcur_node1 = backoff1['backoffcur']

	if backoff2:
		bla.backoffmax_node2 = backoff2['backoffmax']
		bla.backoffcur_node2 = backoff2['backoffcur']

