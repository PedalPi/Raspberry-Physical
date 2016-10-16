from enum import Enum


class MessageType(Enum):

    ACK = "ack"
    EFFECT = "effect"
    PARAM = "param"
    PATCH = "patch"
    ERROR = "error"
