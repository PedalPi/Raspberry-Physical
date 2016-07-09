# -*- coding: utf-8 -*-
from gpiozero import Button, LED


class EffectComponent(object):
    __effect = None

    def __init__(self, pinButton, pinLed, twoState=True):
        self.button = Button(pinButton)
        self.led = LED(pinLed)
        self.twoState = twoState

    @property
    def action(self):
        return self.button.when_pressed

    @action.setter
    def action(self, data):
        self.button.when_pressed = lambda: [data(), self.led.toggle()]

    @property
    def effect(self):
        return self.__effect

    @effect.setter
    def effect(self, effect):
        """
        Update this component status by :param effect
        """
        self.__effect = effect
        if effect.status:
            self.led.on()
        else:
            self.led.off()

    def active(self):
        pass

    def disable(self):
        pass
