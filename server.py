#!/usr/bin/python
# Copyright (c) 2001-2004 Twisted Matrix Laboratories.
# See LICENSE for details.

#

from twisted.internet.protocol import Protocol, Factory
#from twisted.protocols.basic import NetstringReceiver
from twisted.internet import reactor
import handler

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

	handler.handle(self.buffer)



def main():
    f = Factory()
    f.protocol = Echo
    reactor.listenTCP(23415, f)
    reactor.run()

if __name__ == '__main__':
    main()
