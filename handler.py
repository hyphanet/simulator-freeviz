import db
import parser
import time

timedelta=360

def handle(data):
	(nodeinfo, nodeinfos, backoffs)=parser.parse(data)
	#deleting first
	if 'identity' in nodeinfo:
		db.refresh(nodeinfo)
		db.delete_conns(nodeinfo)
		if nodeinfos:
			for nodeinfo2 in nodeinfos:
				db.refresh(nodeinfo2)

				if nodeinfo['identity'] in backoffs:
					backoff1 = backoffs[ nodeinfo['identity']]
				else:
					backoff1={}

				if nodeinfo2['identity'] in backoffs:
					backoff2 = backoffs[ nodeinfo2['identity'] ]
				else:
					backoff2= {}

				db.insert(nodeinfo,nodeinfo2, backoff1=backoff1, backoff2=backoff2)
	check_nodes()


#check if the node is up to date, if not remove it from node-pairs
def check_nodes():
	nodes = db.Node.select()

	for node in nodes:
		if inactive(node):
			nodeinfo = getInfoFromNode(node)
			db.delete_conns(nodeinfo)


def inactive(node):
	nodetime = node.lastUpdate
	return (curtime() - convtime(nodetime) ) > timedelta


def get_activenodes():
	nodes = db.Node.select()
	active_nodes=[]

	for node in nodes:
		if not inactive(node):
			active_nodes.append(node)

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
