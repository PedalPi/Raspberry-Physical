import json


class Message(object):

    def __init__(self, message_type, content=None):
        """
        :param MessageType message_type:
        :param dict content:
        """
        self.message_type = message_type
        self.content = content

    def has_content(self):
        return self.content is not None

    def __str__(self):
        if self.has_content():
            return str(self.message_type) + " " + json.dumps(self.content) + "\n"
        else:
            return str(self.message_type) + "\n"

    def __getitem__(self, key):
        return self.content[key]
