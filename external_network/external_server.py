from twisted.internet import protocol, reactor

transport = set()
class Chat(protocol.Protocol):
    def connectionMade(self):
        #self.transport.write('cop'.encode())
        print('connnn')
        transport.add(self.transport)
    def dataReceived(self, data):
        for t in transport:
            if self.transport is not t:
                t.write(data)
        print(data.decode())
        #self.transport.write(data)

class ChatFactory(protocol.Factory):
    def buildProtocol(self, addr):
        return Chat()

print('Server started!')
reactor.listenTCP(8001, ChatFactory())
reactor.run()