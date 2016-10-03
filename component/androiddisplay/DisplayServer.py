import tornado.gen
import tornado.ioloop
import tornado.iostream
import tornado.tcpserver

from component.androiddisplay.DisplayClient import DisplayClient


class DisplayServer(tornado.tcpserver.TCPServer):
    """
    Example use

    ```
    host = '0.0.0.0'
    port = 10000

    server = DisplayServer()
    server.listen(port, host)
    print("Listening on %s:%d..." % (host, port))
    ```
    """

    clients = []

    @tornado.gen.coroutine
    def handle_stream(self, stream, address):
        """
        Called for each new connection, stream.socket is
        a reference to socket object
        """
        client = DisplayClient(stream)
        self.clients.append(client)
        yield client.on_connect()

    def send(self, message):
        for client in self.clients:
            client.stream.write(message, lambda: print("Message has been send", message))
