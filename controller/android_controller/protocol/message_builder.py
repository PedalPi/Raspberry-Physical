import json

from physical.controller.android_controller.protocol.message_type import MessageType
from physical.controller.android_controller.protocol.message import Message


class MessageBuilder(object):
    @staticmethod
    def generate(message):
        strings = message.split(" ")

        protocol_type = MessageBuilder.search_type(strings[0])

        return MessageBuilder.generate_message(strings, protocol_type)

    @staticmethod
    def search_type(word):
        for protocol_type in MessageType:
            if protocol_type.value == word:
                return protocol_type

        return MessageType.ERROR

    @staticmethod
    def generate_message(strings, protocol_type):
        if len(strings) == 2:
            return Message(protocol_type, json.loads(strings[1]))
        else:
            return Message(protocol_type)
