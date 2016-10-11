# -*- coding: utf-8 -*-
from component.PatchComponent import PatchComponent
from component.PCD8544DisplayComponent import PCD8544DisplayComponent
from component.SevenSegmentsDisplay import SevenSegmentsDisplay
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
        self.display = SevenSegmentsDisplay(a=13, b=6, c=16, d=20, e=21, f=19, g=26, dp=0, common_unit=5, common_tens=1)
        #self.display = PCD8544DisplayComponent(1, 2, 3, 4, 5)
        #self.display = AndroidDisplay('localhost', 10000)

        # Patch
        self.nextPatchButton = PatchComponent(15)
        self.beforePatchButton = PatchComponent(18)

        # Effect
        self.effectButton = EffectComponent(pin_button=26, pin_led=21)

        # DigitalEncoder
        self.digitalEncoder = RotaryEncoderWithButton(pin_a=19, pin_b=13, button_pin=6, pull_up=True)
