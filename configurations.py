# -*- coding: utf-8 -*-
from component.displays_component import DisplayComponent
from component.patch_component import PatchComponent
#from component.PCD8544DisplayComponent import PCD8544DisplayComponent
from component.sevensegments.seven_segments_display import SevenSegmentsDisplay
from component.effect_component import EffectComponent
from component.rotary_encoder import RotaryEncoderWithButton
from gpiozero.pins.mock import MockPin


class Configurations(object):
    """
    Configure the pins based in
    https://pinout.xyz/ pinout number
    """
    displays = None
    next_patch_button = None
    before_patch_button = None
    effect_button = None
    rotary_encoder = None

    def __init__(self, test=False):
        if test:
            self.test()
        else:
            self.configure()

    def configure(self):
        self.displays = DisplayComponent()
        self.displays.append(SevenSegmentsDisplay(a=13, b=6, c=16, d=20, e=21, f=19, g=26, dp=0, common_unit=5, common_tens=1))
        #self.displays.append(DisplayViewClient('localhost', 10000))
        #self.displays.append(PCD8544DisplayComponent(1, 2, 3, 4, 5))

        self.next_patch_button = PatchComponent(14)
        self.before_patch_button = PatchComponent(15)

        self.effect_button = EffectComponent(pin_button=MockPin(40), pin_led=MockPin(41))

        self.rotary_encoder = RotaryEncoderWithButton(pin_a=MockPin(42), pin_b=MockPin(43), button_pin=MockPin(44), pull_up=True)

    def test(self):
        # Display
        self.displays = DisplayComponent()
        self.displays.append(
            SevenSegmentsDisplay(
                a=MockPin(13), b=MockPin(6), c=MockPin(16),
                d=MockPin(20), e=MockPin(21), f=MockPin(19),
                g=MockPin(26), dp=MockPin(0),
                common_unit=MockPin(5),
                common_tens=MockPin(1)
            )
        )
        #self.displays.append(PCD8544DisplayComponent(1, 2, 3, 4, 5))

        self.next_patch_button = PatchComponent(MockPin(15))
        self.before_patch_button = PatchComponent(MockPin(18))

        self.effect_button = EffectComponent(pin_button=MockPin(28), pin_led=MockPin(29))

        self.rotary_encoder = RotaryEncoderWithButton(
            pin_a=MockPin(30),
            pin_b=MockPin(31),
            button_pin=MockPin(32),
            pull_up=True
        )
