import socket

import tornado.gen
import tornado.ioloop
import tornado.iostream
import tornado.tcpserver


class DisplayClient(object):
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

    def __init__(self, stream):
        self.stream = stream

        self.stream.socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        self.stream.socket.setsockopt(socket.IPPROTO_TCP, socket.SO_KEEPALIVE, 1)
        self.stream.set_close_callback(self.on_disconnect)

    @tornado.gen.coroutine
    def on_disconnect(self):
        self.log("disconnected")
        yield []

    @tornado.gen.coroutine
    def dispatch_client(self):
        try:
            while True:
                line = yield self.stream.read_until(b'\n')
                self.log('got |%s|' % line.decode('utf-8').strip())
                yield self.stream.write(line)
        except tornado.iostream.StreamClosedError:
            pass

    @tornado.gen.coroutine
    def on_connect(self):
        raddr = 'closed'
        try:
            raddr = '%s:%d' % self.stream.socket.getpeername()
        except Exception:
            pass

        self.log('new, %s' % raddr)

        yield self.dispatch_client()

    def log(self, msg, *args, **kwargs):
        print('[connection x] %s' % (msg.format(*args, **kwargs)))


class DisplayServer(tornado.tcpserver.TCPServer):
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
            client.stream.write(message, lambda : print("sended", message))
