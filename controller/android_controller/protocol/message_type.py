from enum import Enum


class MessageType(Enum):

    ACK = "ack"
    EFFECT = "effect"
    PARAM = "param"
    PATCH = "patch"
    ERROR = "error"

    def __str__(self):
        return self.value
