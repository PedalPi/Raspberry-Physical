# -*- coding: utf-8 -*-
from component.PatchComponent import PatchComponent
from component.PCD8544DisplayComponent import PCD8544DisplayComponent
from component.EffectComponent import EffectComponent
from component.DigitalEncoder import DigitalEncoder


class Configurations(object):
    """
    Configure the pins based in
    https://pinout.xyz/ pinout number
    """

    def __init__(self):
        # Display
        self.display = None#PCD8544DisplayComponent(1, 2, 3, 4, 5)

        # Patch
        self.nextPatchButton = PatchComponent(15)
        self.beforePatchButton = PatchComponent(18)

        # Effect
        self.effectButton = EffectComponent(pinButton=26, pinLed=21)

        # DigitalEncoder
        self.digitalEncoder = DigitalEncoder(None, None, None)
