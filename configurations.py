# -*- coding: utf-8 -*-
from component.PatchButton import PatchButton
from component.PCD8544DisplayComponent import PCD8544DisplayComponent
from component.EffectComponent import EffectComponent
from component.DigitalEncoder import DigitalEncoder


class Configurations(object):
    """
    Configure the pins based in
    https://pinout.xyz/ pinout number (because GPIOZero)
    """

    def __init__(self):
        # Display
        self.display = None#PCD8544DisplayComponent(1, 2, 3, 4, 5)

        # Patch
        self.nextPatchButton = PatchButton(21)
        self.beforePatchButton = PatchButton(20)

        # Effect
        self.effectButton = EffectComponent(Button(4), LED(5))

        # DigitalEncoder
        self.digitalEncoder = DigitalEncoder(1, 2, 3)
