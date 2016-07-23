import asyncio

import time


class Server(asyncio.Protocol):
    transport = None
    address = None
    clients = None

    def __init__(self):
        self.clients = []

    def connection_made(self, transport):
        self.clients.append(transport)
        self.address = transport.get_extra_info('peername')
        print("Client connected -", self.address)

    def sendAll(self, data):
        for client in self.clients:
            client.write(data)

    def data_received(self, data):
        self.transport.write(data)

    def eof_received(self):
        if self.transport.can_write_eof():
            self.transport.write_eof()

    def connection_lost(self, error):
        if error:
            print('ERROR: {}'.format(error))
        else:
            print('Closing connection')

        super().connection_lost(error)

# Create the server and let the loop finish the coroutine before
# starting the real event loop.
SERVER_ADDRESS = ('localhost', 10000)

event_loop = asyncio.get_event_loop()

factory = event_loop.create_server(Server, *SERVER_ADDRESS)
server = event_loop.run_until_complete(factory)
print('starting up on {} port {}'.format(*SERVER_ADDRESS))

# Enter the event loop permanently to handle all connections.
'''
try:
    while True:
        print('sending data')
        print(server.clients)
        server.sendAll(b'effect {"index": 5, name="PedalBoard"}\n')
        #{"name": "ratio", "min": 0, "max": 10, "current": 5}
        time.sleep(20)
finally:
    print('closing server')
    server.close()
    event_loop.run_until_complete(server.wait_closed())
    print('closing event loop')
    event_loop.close()
'''

try:
    event_loop.run_forever()
    print('test')
finally:
    print('closing server')
    server.close()
    event_loop.run_until_complete(server.wait_closed())
    print('closing event loop')
    event_loop.close()

'''
print('starting up on %s port %s' % serverAddress)
socket.bind(serverAddress)
socket.listen(1)

while True:
    print('waiting for a connection')
    connection, client_address = sock.accept()

    try:
        print('client connected:', client_address)

        while True:
            print('sending data')
            connection.sendall(b'effect {"index": 5, name="PedalBoard"}\n')
            time.sleep(20)
    finally:
        connection.close()

'''