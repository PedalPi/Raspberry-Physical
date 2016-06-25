# -*- coding: utf-8 -*-


class DigitalEncoder(object)

    class DigitalState(Enum):
        NEXT(1)
        BEFORE(-1)

    def __init__(self, minuPin, plusPin, selectPin):
        self.minusPin = minusPin
        self.plusPin = plusPin
        self.selectPin = selectPin

        #self.config.effects[0].action = currentActions.setEffectParam

    @param
    def lastState(self):
        return DigitalState.NEXT
