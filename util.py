from message import Message
from message_type import MessageType


def send_and_confirm(conn, msg: Message):
    """
    Sends a message and waits for confirm that it received
    or has been processed. This is necessary to make sure
    ports are open before attempting to connect.
    :param conn: the connection to send to.
    :param msg: the message to send and have confirmed.
    """
    conn.send(msg.encode())
    data = conn.recv(1024)
    message = Message.decode(data)
    assert message.message_type == MessageType.CLIENT_CONFIRM
