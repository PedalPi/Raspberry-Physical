from physical.controller.android_controller.protocol.message_type import MessageType
from physical.controller.android_controller.protocol.message import Message

from application.model.UpdatesObserver import UpdatesObserver


class AndroidUpdatesObserver(UpdatesObserver):
    def __init__(self, client):
        self.client = client

    def onBankUpdate(self, bank, update_type, token=None):
        pass

    def onParamValueChange(self, param, token=None):
        pass

    def onEffectStatusToggled(self, effect, token=None):
        pass

    def onEffectUpdated(self, effect, update_type, token=None):
        pass

    def onCurrentPatchChange(self, patch, token=None):
        message = Message(MessageType.PATCH, patch)
        self.client.send(message)

    def onPatchUpdated(self, patch, update_type, token=None):
        pass
