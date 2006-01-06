import db

def get():
	data=[]
	connections = list(db.NodePair.select())

	for conn in connections:
		left={}
		right={}
		left['identity'] = conn.node1.identity
		left['location'] = conn.node1.location

		right['identity'] = conn.node2.identity
		right['location'] = conn.node2.location
		data.append( (left, right) )

	return data
		
