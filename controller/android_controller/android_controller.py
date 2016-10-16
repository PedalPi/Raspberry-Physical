from physical.controller.android_controller.android_controller_client import AndroidControllerClient
from physical.controller.android_controller.android_updates_observer import AndroidUpdatesObserver
from physical.controller.android_controller.protocol.message_type import MessageType

from physical.base.controller import Controller

from application.controller.EffectController import EffectController
from application.controller.ParamController import ParamController

import os


class AndroidController(Controller):
    def __init__(self, application):
        super(AndroidController, self).__init__(application, self.__class__.__name__)
        self.client = AndroidControllerClient('localhost', 8888)
        self.observer = AndroidUpdatesObserver(self.client)

    def init(self):
        self.start_android_application()
        self.client.message_listener = self.process_message
        self.register_observer(self.observer)
        self.client.run()

    def start_android_application(self):
        activity = 'io.github.pedalpi.pedalpidisplay/io.github.pedalpi.pedalpidisplay.EffectsActivity'
        port = 8888

        os.system('adb shell am start -n ' + activity)
        os.system('adb forward --remove-all')
        os.system('adb forward tcp:' + str(port) + ' tcp:' + str(port))

    def process_message(self, message):
        print("Message received:", message)

        if message.message_type == MessageType.PARAM:
            controller = self.controller(ParamController)
            #controller.updateValue(param, new_value, self.token)

        elif message.message_type == MessageType.EFFECT:
            controller = self.controller(EffectController)
            #controller.toggleStatus(effect, self.token)
