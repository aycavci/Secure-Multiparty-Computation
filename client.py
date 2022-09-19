import socket
from time import sleep

from client_receive_handler import ReceiveHandler
from message import Message
from message_type import MessageType
import mpc


class Client:
    def __init__(self):
        self.soc = socket.socket()  # for server communication
        self.receiver = ReceiveHandler(self.receive)  # for receiving messages
        self.soc_out = socket.socket()  # for sending messages
        self.host_port = -1
        self.send_port = -1
        self.share = 0
        self.r = 0

    def setup_connection(self):
        # Connect to server
        server_port = 3000
        self.soc.connect(('localhost', server_port))

        try:
            # Receive the given port number
            while True:
                data = self.soc.recv(1024)
                msg = Message.decode(data)

                if msg.message_type == MessageType.CLIENT_BIND_PORT:
                    self.host_port = int(msg.message)
                    self.receiver.bind(self.host_port)
                    self.soc.send(Message(MessageType.CLIENT_CONFIRM).encode())
                elif msg.message_type == MessageType.CLIENT_SET_SEND_PORT:
                    self.send_port = int(msg.message)
                    self.soc.send(Message(MessageType.CLIENT_CONFIRM).encode())
                elif msg.message_type == MessageType.CLIENT_AWAIT_SHARE:
                    self.soc.send(Message(MessageType.CLIENT_CONFIRM).encode())
                    # Receive share from data owner
                    self.receiver.soc.listen(1)
                    owner_conn, _ = self.receiver.soc.accept()
                    data = owner_conn.recv(1024)
                    msg = Message.decode(data)
                    self.share = int(msg.message)
                    owner_conn.send(Message(MessageType.CLIENT_CONFIRM).encode())
                    print("Initial share: ", self.share)
                elif msg.message_type == MessageType.ACCEPT_THEN_CONNECT:
                    self.soc.send(Message(MessageType.CLIENT_CONFIRM).encode())
                    self.receiver.accept_incoming()
                    self.soc_out.connect(('localhost', self.send_port))
                    print(self.host_port, self.send_port)
                    break
                elif msg.message_type == MessageType.CONNECT_THEN_ACCEPT:
                    self.soc.send(Message(MessageType.CLIENT_CONFIRM).encode())
                    self.soc_out.connect(('localhost', self.send_port))
                    self.receiver.accept_incoming()
                    print(self.host_port, self.send_port)
                    break

            self.receiver.start()
        except Exception as e:
            print(e)
            raise e

    def receive(self, msg: Message):
        print("Received: ", msg.message)
        sleep(0.5)

        if self.host_port != 3001:
            # c(1) has already generated their r(1) before.
            self.r = mpc.generate_random_number()

        # Where w(i) = u(i) + r(sent) - r(receive) calculated.
        self.share = self.share + self.r - int(msg.message)
        print("Updated share: ", self.share, ", r value used: ", self.r)

        if self.host_port == 3001:
            # Update r(1) because inverse order of operations.
            self.r = mpc.generate_random_number()

        # Where r generated by c(i) is sent to the c(i+1)
        self.soc_out.send(Message(MessageType.CLIENT_MESSAGE, str(self.r)).encode())

    def run(self):
        if self.host_port == 3001:
            # Have c(1) start the daisy-chain for demonstrational purposes.
            self.r = mpc.generate_random_number()
            self.soc_out.send(Message(MessageType.CLIENT_MESSAGE, str(self.r)).encode())
        # Hold until the thread terminates, then terminate the program.
        self.receiver.join()


def main():
    client = Client()
    client.setup_connection()
    client.run()


if __name__ == '__main__':
    main()