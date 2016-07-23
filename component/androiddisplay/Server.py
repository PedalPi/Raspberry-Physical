"""
https://github.com/python/asyncio/blob/master/examples/simple_tcp_server.py

Example of a simple TCP server that is written in (mostly) coroutine
style and uses asyncio.streams.start_server() and
asyncio.streams.open_connection().

Note that running this example starts both the TCP server and client
in the same process.  It listens on port 12345 on 127.0.0.1, so it will
fail if this port is currently in use.
"""

import sys
import asyncio
import asyncio.streams

import time
from threading import Thread


class Server:
    """
    This is just an example of how a TCP server might be potentially
    structured.  This class has basically 3 methods: start the server,
    handle a client, and stop the server.

    Note that you don't have to follow this structure, it is really
    just an example or possible starting point.
    """

    def __init__(self):
        # encapsulates the server sockets
        self.server = None

        # this keeps track of all the clients that connected to our
        # server.  It can be useful in some cases, for instance to
        # kill client connections or to broadcast some data to all
        # clients...
        self.clients = {}  # task -> (reader, writer)

    def send(self, message):
        for reader, writer in self.clients.values():
            writer.write(message)

    def accept_client(self, client_reader, client_writer):
        """
        This method accepts a new client connection and creates a Task
        to handle this client.
        self.clients is updated to keep track of the new client.
        """
        print('Client connected')
        task = asyncio.Task(self.handle_client(client_reader, client_writer))
        self.clients[task] = (client_reader, client_writer)

        task.add_done_callback(self.client_done)

    def client_done(self, task):
        print("client task done:", task)
        del self.clients[task]

    @asyncio.coroutine
    def handle_client(self, client_reader, client_writer):
        """
        This method actually does the work to handle the requests for
        a specific client. The protocol is line oriented, so there is
        a main loop that reads a line with a request and then sends
        out one or more lines back to the client with the result.
        """
        while True:
            data = (yield from client_reader.readline()).decode("utf-8")
            if not data:# an empty string means the client disconnected
                break
            else:
                print("Bad command {!r}".format(data), file=sys.stderr)

            # This enables us to have flow control in our connection.
            yield from client_writer.drain()

    def start(self, loop, address, port):
        """
        Starts the TCP server, so that it listens on port 12345.

        For each client that connects, the accept_client method gets
        called.  This method runs the loop until the server sockets
        are ready to accept connections.
        """
        event = asyncio.streams.start_server(
            self.accept_client,
            address,
            port,
            loop=loop
        )

        self.server = loop.run_until_complete(event)

    def stop(self, loop):
        """
        Stops the TCP server, i.e. closes the listening socket(s).

        This method runs the loop until the server sockets are closed.
        """
        if self.server is not None:
            self.server.close()
            loop.run_until_complete(self.server.wait_closed())
            self.server = None





def threaded_function(server):
    i = 0
    while True:
        if i % 3 == 0:
            message = b'param {"name": "ratio", "min": 0, "max": 10, "current": 5}\n'
        elif i % 3 == 1:
            message = b'effect {"index": 2, name="Macarronada"}\n'
        else:
            message = b'effect {"index": 52, name="Pedalboard"}\n'
        print("Data sended")
        print("Message", message)
        server.send(message)

        time.sleep(10)

        i += 1


def main():
    loop = asyncio.get_event_loop()

    server = Server()
    server.start(loop, 'localhost', 10000)
    print("Server started")

    Thread(target=threaded_function, args=[server]).start()

    try:
        loop.run_until_complete(server.server.wait_closed())
    finally:
        server.stop(loop)
        loop.close()

main()
