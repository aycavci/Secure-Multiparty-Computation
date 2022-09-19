from message_type import MessageType


class Message:
    """
    A message to be sent over network. It can encode and decode itself
    to abstract away the handling of binary encoding.
    """
    def __init__(self, message_type: MessageType, message: str = '-'):
        self.message_type = message_type
        self.message = message

    def encode(self) -> bytes:
        return f'{self.message_type}:{self.message}'.encode()

    @staticmethod
    def decode(message: bytes):
        decoded = message.decode().split(':')
        t, m = decoded
        return Message(MessageType(int(t)), m)
