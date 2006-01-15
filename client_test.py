import socket
import threading
import time
import sys

ADDR=('213.83.30.166',23415)
DELAY=1
MAXCONNS=10
DATA='''
lastGoodVersion=Fred,0.7,1.0,356
physical.udp=85.225.113.27:11717
identity=61cf3d4663ce7325b3748ff2d38dfc823580f87f82af0801c5e2cf20d60593e2
myName=cyberdo
location=0.2754721275879277
testnetPort=12717
testnet=true
version=Fred,0.7,1.0,356
End



requests=0
transferring_requests=0
inserts=4
CONNECTED    128.100.171.30:4000 PVT 0.47973367104523934 Fred,0.7,1.0,356 backoff: 5000 (0)|037cac004e87930b5a9483a3ad0e8fb720088f223873015b7dd6109a7d21102d
CONNECTED    192.168.10.117:11718 cyberdo_slave2 0.26733658819830175 Fred,0.7,1.0,356 backoff: 5000 (0)|ac6344b4f874872ffc97944e4e6eee2ed46f4dbf69af2822283612359e3a1e6c
CONNECTED    192.168.10.117:11719 cyberdo_slave3 0.26462456118755406 Fred,0.7,1.0,356 backoff: 5000 (0)|46c2a07ded3760f28527a613961bf0cf07f854966b5974591b701a5beb9494d6
CONNECTED    209.6.82.6:55555 mikeDOTd 0.45133906442280003 Fred,0.7,1.0,356 backoff: 5000 (0)|2e65ea47332c70def8baabedf315374a4ceecdde92cdd7dc5d2aa731bee49120
CONNECTED    212.202.175.197:12313 TheBishop1 0.29276802951395575 Fred,0.7,1.0,356 backoff: 5000 (0)|c4c0b2f6a4409d7cf6d729cb2eabc76922cb5006e1300a069012812b5319f8bc
DISCONNECTED 192.168.10.117:1337 cyberdo_devel 0.3902854008904836 Fred,0.7,1.0,305 backoff: 5000 (0)|85101e6f9a884bdd579cb5d9cf0ab0bd4d0d4807691ee771986b861e35b7b761
DISCONNECTED 194.231.78.1:4000 Jogy 0.2754721275879277 Fred,0.7,1.0,356 backoff: 5000 (0)|3ef1ecf44a7cf2d061845c84871d8b8188d0d820e913a1e27e3fa9e4d51e7268
DISCONNECTED 206.248.152.124:4000 PVT-TEST1 0.4878134854007906 Fred,0.7,1.0,336 backoff: 5000 (0)|f144277b991e3c3709423db0fd84aa443c257ea0e1dff4b9d319b4649b30135f
DISCONNECTED 212.202.175.197:28115 mistmade2 0.2964722472278719 Fred,0.7,1.0,356 backoff: 5000 (0)|c4b5592366b10891d2b7264a87fb2968131ac405429a90c5eef21801b502a1c4
DISCONNECTED 217.210.202.34:14287 warpi 0.49699446674423164 Fred,0.7,1.0,356 backoff: 5000 (0)|802e9865e188c8ab485b611fad7661c1543e140e750ecb3456bdb35b3ce36c0d
'''

class Base(threading.Thread):
	vlock = threading.Lock()
	id=0
	conns = 0 


class clnt(Base):
	def __init__(self,data):
		threading.Thread.__init__(self)
		self.clnsock= socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		self.myid=Base.id
		Base.id+=1
		self.data = data


	def run(self):
		self.clnsock.connect(ADDR)
		self.clnsock.sendall(self.data)
		self.clnsock.shutdown(socket.SHUT_RDWR)
		self.clnsock.close()
		Base.vlock.acquire()
		Base.conns -= 1
		Base.vlock.release()	


try:
	while 1:
		threading.Lock().acquire()
		conns = Base.conns
		threading.Lock().release
		print "conns running %d" % conns
	
		if conns < MAXCONNS:
			c = clnt(DATA)
			threading.Lock().acquire()
			Base.conns += 1
			threading.Lock().release
			c.start()	
		else:
			print "DELAY!"
			time.sleep(DELAY)
except KeyboardInterrupt:
	sys.exit(1)
