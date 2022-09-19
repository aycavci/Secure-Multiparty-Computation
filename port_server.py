import socket

from message import Message
from message_type import MessageType
from util import send_and_confirm

REQUIRED_CONNECTIONS = 3  # The number of participants in the ring (hard-coded)

if __name__ == '__main__':
    soc = socket.socket()
    port = 3000  # Server runs on port 3000
    soc.bind(('localhost', port))

    first_port = 3001  # clients run on ports 3001 and onwards

    # The connections we establish. Every element is connected to the next
    # by the end of the program. The last is connected back to the first.
    ports = []
    connections = []

    try:
        # Await data owner connection
        soc.listen()
        owner_conn, _ = soc.accept()  # accept join request

        # Await all incoming connections
        while len(connections) < REQUIRED_CONNECTIONS:
            soc.listen()
            conn, _ = soc.accept()  # accept join request

            if not ports:
                port = first_port
                ports.append(port)
            else:
                port = ports[-1] + 1
                ports.append(port)

            # Send host port to client and let them bind to it.
            send_and_confirm(conn, Message(MessageType.CLIENT_BIND_PORT, str(port)))
            connections.append(conn)

        # Instruct all clients to await their share.
        for conn in connections:
            send_and_confirm(conn, Message(MessageType.CLIENT_AWAIT_SHARE))
        # Instruct data owner to distribute shares among all clients (as a outside party).
        str_ports = ','.join([str(p) for p in ports])
        send_and_confirm(owner_conn, Message(MessageType.OWNER_RECEIVE_PORTS, str_ports))

        #  Send clients ports to create the ring
        print('Sending next in ring ports')
        for i, conn in enumerate(connections):
            send_and_confirm(conn, Message(MessageType.CLIENT_SET_SEND_PORT,
                                           str(ports[(i + 1) % len(connections)])))

        # Setup the connections.
        print('Establish connections')
        for i, conn in enumerate(connections[1:]):
            # First set every connection but the first to accept connections,
            # after which they will attempt to the next connect to the next in the ring.
            # Sends u values (shares) to the corresponding client (first element in the
            # u_array goes to first client, second goes to second client etc.)
            send_and_confirm(conn, Message(MessageType.ACCEPT_THEN_CONNECT))
        # Have the first connection connect to the second in the ring, starting
        # a daisy-chain of connections connecting to the next in the ring.
        send_and_confirm(connections[0], Message(MessageType.CONNECT_THEN_ACCEPT))

    finally:
        # Ensure that the sockets are closed on failure.
        soc.close()
        for conn in connections:
            conn.close()
