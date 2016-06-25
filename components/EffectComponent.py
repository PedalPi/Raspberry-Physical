# -*- coding: utf-8 -*-
from gpiozero import Button, LED


class EffectComponent(object):

    def __init__(self, pinButton, pinLed, twoState=True)
        self.button = Button(pinButton)
        self.led = LED(pinLed)
        self.twoState = twoState

    @action.setter
    def action(self, data)
        self.button.when_pressed = lambda:
            data()
            self.led.toggle()

    @action.effect
    def effect(self, effect):
        '''
        Update this component status by @param effect
        '''
        if effect['active']:
            self.led.on()
        else:
            self.led.off()

    def active():
        pass

    def disable():
        pass
