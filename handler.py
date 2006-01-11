import db
import parser
import time

timedelta=360

def handle(data,trans):
	(nodeinfo, nodeinfos, backoffs)=parser.parse(data)

	#deleting first
	if 'identity' in nodeinfo:
		db.refresh(nodeinfo,trans)
		db.delete_conns(nodeinfo,trans)
		if nodeinfos:
			for nodeinfo2 in nodeinfos:
				db.refresh(nodeinfo2,trans)

				if nodeinfo['identity'] in backoffs:
					backoff1 = backoffs[ nodeinfo['identity']]
				else:
					backoff1={}

				if nodeinfo2['identity'] in backoffs:
					backoff2 = backoffs[ nodeinfo2['identity'] ]
				else:
					backoff2= {}

				db.insert(trans, nodeinfo,nodeinfo2, backoff1=backoff1, backoff2=backoff2)
	check_nodes(trans)
	
	#FINISHING TRANSACTION
	trans.commit()

#check if the node is up to date, if not remove it from node-pairs
def check_nodes(trans):
	nodes = db.Node.select(connection=trans)

	for node in nodes:
		if inactive(node):
			nodeinfo = getInfoFromNode(node)
			db.delete_conns(nodeinfo,trans)
			node.active='N'
		else:
			node.active='Y'

def inactive(node):
	nodetime = node.lastUpdate
	return (curtime() - convtime(nodetime) ) > timedelta


def get_activenodes(trans):
	active_nodes = list(db.Node.select( db.Node.q.active == 'Y', connection=trans))

	return active_nodes

#time in seconds since epoch
def curtime():
	return time.time()

def getInfoFromNode(node):
	nodeinfo={}
	nodeinfo['name']=node.name
	nodeinfo['version']=node.version
	nodeinfo['identity']=node.identity

	return nodeinfo

#convert timeformat of lastupdated db entry to seconds
#maybe it belongs to db module
def convtime(lastUpdate):
	ttuple = lastUpdate.timetuple()
	return time.mktime(ttuple)
