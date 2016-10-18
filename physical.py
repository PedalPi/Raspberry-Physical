# -*- coding: utf-8 -*-
from physical.controller.pedal_zero_controller.pedal_zero_controller import PedalZeroController
from physical.controller.android_controller.android_controller import AndroidController


class Physical(object):

    def __init__(self, application, test=False):
        self.app = application
        self.controllers = [
            PedalZeroController(application, test),
            AndroidController(application)
        ]

        self.start(self.controllers)

    def start(self, controllers):
        for controller in controllers:
            controller.init()
