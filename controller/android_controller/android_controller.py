from physical.controller.android_controller.android_controller_client import AndroidControllerClient
from physical.controller.android_controller.android_updates_observer import AndroidUpdatesObserver
from physical.controller.android_controller.protocol.message_type import MessageType

from physical.base.controller import Controller

from application.controller.CurrentController import CurrentController
from application.controller.EffectController import EffectController
from application.controller.ParamController import ParamController

import os


class AndroidController(Controller):
    def __init__(self, application):
        super(AndroidController, self).__init__(application, self.__class__.__name__)
        self.client = AndroidControllerClient('localhost', 8888)
        self.observer = AndroidUpdatesObserver(self.client, self.token)

    def init(self):
        self.start_android_application()
        self.client.message_listener = self.process_message
        self.register_observer(self.observer)
        self.client.run()

    def start_android_application(self):
        activity = 'com.pedalpi.pedalpi/com.pedalpi.pedalpi.PatchActivity'
        port = 8888

        os.system('adb shell am start -n ' + activity)
        os.system('adb forward --remove-all')
        os.system('adb forward tcp:' + str(port) + ' tcp:' + str(port))

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
