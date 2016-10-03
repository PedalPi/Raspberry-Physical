# -*- coding: utf-8 -*-
from component.PatchComponent import PatchComponent
from component.PCD8544DisplayComponent import PCD8544DisplayComponent
from component.EffectComponent import EffectComponent
from component.RotaryEncoder import RotaryEncoderWithButton
from component.androiddisplay.AndroidDisplay import AndroidDisplay


class Configurations(object):
    """
    Configure the pins based in
    https://pinout.xyz/ pinout number
    """

    def __init__(self):
        # Display
        self.display = None#PCD8544DisplayComponent(1, 2, 3, 4, 5)
        self.display = AndroidDisplay('localhost', 10000)

        # Patch
        self.nextPatchButton = PatchComponent(15)
        self.beforePatchButton = PatchComponent(18)

        # Effect
        self.effectButton = EffectComponent(pin_button=26, pin_led=21)

        # DigitalEncoder
        self.digitalEncoder = RotaryEncoderWithButton(pin_a=19, pin_b=13, button_pin=6, pullUp=True)
