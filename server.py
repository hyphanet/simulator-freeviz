import socket
import threading
import handler
import db
import time

PORT=23415
NRCONS=100
DELAY=1
MAXCONNS=10


class Base(threading.Thread):
	vlock = threading.Lock()
	chunks=[]
	id=0
	conns = 0 

class Handler(Base):
	

	def run(self):
		con = db.get_con()		
		trans = con.transaction()
		while 1:
			Base.vlock.acquire()
			for chunk in Base.chunks:
				handler.handle(chunk,trans)
			if Base.chunks: print "COMMITED"
			Base.chunks=[]
			Base.vlock.release()
			time.sleep(DELAY)			

class serv(Base):
	chunk=''
	def __init__(self,clnsock):
		threading.Thread.__init__(self)
		self.clnsock=clnsock
		self.myid=Base.id
		Base.id+=1


	def run(self):
		while 1:
			k = self.clnsock.recv(1024)
			if k == '': break
			self.chunk+=k
		self.clnsock.close()
		Base.vlock.acquire()
		Base.chunks.append(self.chunk)
		Base.conns -= 1
		Base.vlock.release()	
		print "%s\n________\n" % self.chunk


lstn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lstn.bind(('',PORT))
lstn.listen(100)
h = Handler()
h.start()
conns=0
while 1:
	threading.Lock().acquire()
	conns = Base.conns
	threading.Lock().release
	print "conns running %d" % conns

	if conns < MAXCONNS:
		(clnt,ap) = lstn.accept()
		s = serv(clnt)
		threading.Lock().acquire()
		Base.conns += 1
		threading.Lock().release
		s.start()	
	else:
		print "DELAY!"
		time.sleep(1)
