#!/usr/bin/python
# Copyright (c) 2001-2004 Twisted Matrix Laboratories.
# See LICENSE for details.

#

from twisted.internet.protocol import Protocol, Factory
#from twisted.protocols.basic import NetstringReceiver
from twisted.internet import reactor
import handler
import threading


class Handler(threading.Thread):
	data=''
	def __init__(self,data):
		threading.Thread.__init__(self)
		self.data = data	


	def run(self):
		handler.handle(self.data)

### Protocol Implementation

# This is just about the simplest possible protocol
class Echo(Protocol):
    buffer=''
    def dataReceived(self, data):
        """As soon as any data is received, write it back."""
	self.buffer+=data
    def connectionLost(self,reason):
	print self.buffer
	print "_______________________\n\n"

	h = Handler(self.buffer)
	h.start()
	h.join()


def main():
    f = Factory()
    f.protocol = Echo
    reactor.listenTCP(23415, f)
    reactor.run()

if __name__ == '__main__':
    main()
