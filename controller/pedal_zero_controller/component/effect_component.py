# -*- coding: utf-8 -*-
from gpiozero import Button, LED


class EffectComponent(object):
    _effect = None

    def __init__(self, pin_button, pin_led, two_state=True):
        self.button = Button(pin_button, pull_up=False)
        self.led = LED(pin_led)
        self.two_state = two_state

    @property
    def action(self):
        return self.button.when_pressed

    @action.setter
    def action(self, data):
        self.button.when_pressed = lambda: [data(), self.led.toggle()]

    @property
    def effect(self):
        return self._effect

    @effect.setter
    def effect(self, effect):
        """
        Update this component status by :param effect
        """
        self._effect = effect
        if effect.status:
            self.led.on()
        else:
            self.led.off()

    def active(self):
        pass

    def disable(self):
        pass
