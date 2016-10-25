from tornado import gen
from tornado.tcpclient import TCPClient

from physical.controller.android_controller.protocol.message_builder import MessageBuilder


class AndroidControllerClient(object):

    def __init__(self, address, port, encoding="utf-8"):
        self.address = address
        self.port = port
        self.encoding = encoding

        self.stream = None
        self.message_listener = lambda message: print(message)
        self.connected_listener = lambda: ...

    @gen.coroutine
    def run(self):
        self.stream = yield TCPClient().connect(self.address, self.port)
        self.connected_listener()

        while True:
            data = yield self.stream.read_until('\n'.encode(self.encoding))
            data = data.decode(self.encoding).strip()

            self.message_listener(MessageBuilder.generate(data))

    def send(self, message):
        text = str(message).encode(self.encoding)
        self.stream.write(text)
