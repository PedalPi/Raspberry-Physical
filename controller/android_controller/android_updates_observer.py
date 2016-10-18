from physical.controller.android_controller.protocol.message_type import MessageType
from physical.controller.android_controller.protocol.message import Message

from application.model.UpdatesObserver import UpdatesObserver


class AndroidUpdatesObserver(UpdatesObserver):
    def __init__(self, client, token):
        self.client = client
        self.token = token

    def onBankUpdate(self, bank, update_type, token=None):
        pass

    def onParamValueChange(self, param, token=None):
        if token == self.token:
            return

        effect = param.effect

        data = {
            'effect': effect.index,
            'param': param.index,
            'value': param.value
        }
        message = Message(MessageType.PARAM, data)
        self.client.send(message)

    def onEffectStatusToggled(self, effect, token=None):
        if token == self.token:
            return

        message = Message(MessageType.EFFECT, {'index': effect.index})
        self.client.send(message)

    def onEffectUpdated(self, effect, update_type, token=None):
        if token == self.token:
            return

        pass

    def onCurrentPatchChange(self, patch, token=None):
        if token == self.token:
            return

        message = Message(MessageType.PATCH, patch.json)
        self.client.send(message)

    def onPatchUpdated(self, patch, update_type, token=None):
        if token == self.token:
            return

        pass
