# -*- coding: utf-8 -*-
from enum import Enum


class DigitalEncoder(object):
    """
    https://www.circuitsathome.com/mcu/programming/reading-rotary-encoder-on-arduino
    https://github.com/guyc/py-gaugette/blob/master/gaugette/rotary_encoder.py

    http://www.facebook.com/l.php?u=http%3A%2F%2Fabyz.co.uk%2Frpi%2Fpigpio%2Fcode%2Frotary_encoder_py.zip&h=KAQE4xkCc
    http://theatticlight.net/posts/Reading-a-Rotary-Encoder-from-a-Raspberry-Pi/
    """

    class DigitalState(Enum):
        NEXT = 1
        BEFORE = -1

    def __init__(self, minusPin, plusPin, selectPin):
        self.minusPin = minusPin
        self.plusPin = plusPin
        self.selectPin = selectPin

    @property
    def lastState(self):
        return DigitalEncoder.DigitalState.NEXT

    @property
    def minusAction(self):
        return None

    @minusAction.setter
    def minusAction(self, action):
        pass

    @property
    def plusAction(self):
        return None

    @plusAction.setter
    def plusAction(self, action):
        pass

    @property
    def selectAction(self):
        return None

    @selectAction.setter
    def selectAction(self, action):
        pass
