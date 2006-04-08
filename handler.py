import db
import parser
import time
import re

timedelta=360
mandatory_version = 599


def handle(data,trans):
	(nodeinfo, nodeinfos, backoffs)=parser.parse(data)


	#checking the version
	version_parser = re.compile('.*,(\d+)')
	
	if 'version' in nodeinfo:
		version = version_parser.match(nodeinfo['version']).group(1)
		#print "Node version is " + version
		version = int(version)

		#exit when non mandatory version
		if version < mandatory_version:
			print "Skipping following data, because node is too old"
			print data
			return

		
		
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

def get_lastgoodnodes(trans):
	anodes = get_activenodes(trans)
	lastGoodVer = db.getLastGoodVer(trans)
	lgnodes = []

	for anode in anodes:
		if anode.version >= lastGoodVer:
			lgnodes.append(anode)

	return lgnodes

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
