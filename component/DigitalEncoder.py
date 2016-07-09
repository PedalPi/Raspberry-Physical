# -*- coding: utf-8 -*-
from enum import Enum


class DigitalEncoder(object):
    """
    https://www.circuitsathome.com/mcu/programming/reading-rotary-encoder-on-arduino
    https://github.com/guyc/py-gaugette/blob/master/gaugette/rotary_encoder.py
    """

    class DigitalState(Enum):
        NEXT = 1
        BEFORE = -1

    def __init__(self, minusPin, plusPin, selectPin):
        self.minusPin = minusPin
        self.plusPin = plusPin
        self.selectPin = selectPin

        #self.config.effects[0].action = currentActions.setEffectParam

    @property
    def lastState(self):
        return DigitalEncoder.DigitalState.NEXT
