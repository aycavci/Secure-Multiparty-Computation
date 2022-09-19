import socket
from threading import Thread

from message import Message


class ReceiveHandler(Thread):
    """
    Threaded handler to receive incoming packets over socket.
    Calls a callback function using the decoded packet to deliver
    to the parent thread.
    """

    def __init__(self, callback):
        self.callback = callback
        self.soc = socket.socket()
        self.receive_soc = None
        super().__init__()

    def bind(self, port):
        self.soc.bind(('localhost', port))

    def accept_incoming(self):
        self.soc.listen(1)
        self.receive_soc, _ = self.soc.accept()

    def run(self) -> None:
        while True:
            # Busy waiting to listen for incoming data.
            data = self.receive_soc.recv(1024)
            if data:
                msg = Message.decode(data)
                self.callback(msg)

    def close(self):
        self.soc.close()
