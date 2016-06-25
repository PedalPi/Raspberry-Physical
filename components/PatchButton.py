# -*- coding: utf-8 -*-
from gpiozero import Button


class PatchButton(self):
    button = None

    def __init__(self, pin):
        self.button = Button(pin)

    @action.setter
    def action(self, data)
        self.button.when_pressed = data
