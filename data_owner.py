import socket

import mpc
from message import Message
from message_type import MessageType
from port_server import REQUIRED_CONNECTIONS
from util import send_and_confirm


def main():
    # Connect to the server to start the session.
    conn = socket.socket()
    conn.connect(('localhost', 3000))

    # Receive the ports
    data = conn.recv(1024)
    msg = Message.decode(data)
    ports = msg.message.split(',')
    print(ports)

    # Generate u_array which consists u values (shares) determined by client number
    # in the network and sensitive value.
    u_array = mpc.generate_u_array(REQUIRED_CONNECTIONS, 100 * REQUIRED_CONNECTIONS)

    for i, port in enumerate(ports):
        # Connect to each client separately and hand them their share.
        client_conn = socket.socket()
        client_conn.connect(('localhost', int(port)))
        send_and_confirm(client_conn, Message(MessageType.OWNER_SEND_SHARE, u_array[i]))
    conn.send(Message(MessageType.CLIENT_CONFIRM).encode())


if __name__ == '__main__':
    main()
