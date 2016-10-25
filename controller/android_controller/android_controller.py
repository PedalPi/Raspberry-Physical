from physical.controller.android_controller.android_controller_client import AndroidControllerClient
from physical.controller.android_controller.android_updates_observer import AndroidUpdatesObserver
from physical.controller.android_controller.protocol.message_type import MessageType
from physical.controller.android_controller.protocol.message import Message

from physical.base.controller import Controller

from application.controller.CurrentController import CurrentController
from application.controller.EffectController import EffectController
from application.controller.ParamController import ParamController

import os


class AndroidController(Controller):
    def __init__(self, application, adb_command="adb"):
        super(AndroidController, self).__init__(application, self.__class__.__name__)
        self.client = AndroidControllerClient('localhost', 8888)
        self.observer = AndroidUpdatesObserver(self.client, self.token)
        self.adb_command = adb_command

    def init(self):
        self.start_android_application()
        self.client.message_listener = self.process_message
        self.register_observer(self.observer)
        self.client.run()

        self.client.connected_listener = lambda: self.client.send(Message(MessageType.PATCH, self.current_patch.json))

    def start_android_application(self):
        activity = 'com.pedalpi.pedalpi/com.pedalpi.pedalpi.PatchActivity'
        port = 8888

        os.system(self.adb_command + ' shell am start -n ' + activity)
        os.system(self.adb_command + ' forward --remove-all')
        os.system(self.adb_command + ' forward tcp:' + str(port) + ' tcp:' + str(port))

    def process_message(self, message):
        print("Message received:", message)

        current_patch = self.current_patch

        if message.message_type == MessageType.EFFECT:
            effect_index = message['index']
            effect = current_patch.effects[effect_index]

            controller = self.controller(EffectController)
            controller.toggleStatus(effect, self.token)

        elif message.message_type == MessageType.PARAM:
            effect_index = message['effect']
            param_index = message['param']
            value = message['value']

            effect = current_patch.effects[effect_index]
            param = effect.params[param_index]

            controller = self.controller(ParamController)
            controller.updateValue(param, value, self.token)

    @property
    def current_patch(self):
        controller = self.controller(CurrentController)
        return controller.currentPatch
