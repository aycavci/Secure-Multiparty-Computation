import enum


class MessageType(enum.IntEnum):
    """
    Supportive enum to organise message types.
    """
    CLIENT_BIND_PORT = 1
    CLIENT_SET_SEND_PORT = 2
    CONNECT_THEN_ACCEPT = 3
    ACCEPT_THEN_CONNECT = 4
    CLIENT_CONFIRM = 5
    CLIENT_MESSAGE = 6
    OWNER_RECEIVE_PORTS = 7
    OWNER_SEND_SHARE = 8
    CLIENT_AWAIT_SHARE = 9
