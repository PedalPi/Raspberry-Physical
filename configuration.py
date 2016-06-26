# -*- coding: utf-8 -*-
from components import PatchButton


class Configuration(object):

    def __init__(self):
        # Display
        self.display = PCD8544DisplayComponent(1, 2, 3, 4, 5)

        # Patch
        self.nextPatchButton = PatchButton(21)
        self.beforePatchButton = PatchButton(20)

        # Effect
        self.effectButton = EffectButton(Button(4), LED(5))

        # Configuration
        self.manager = ManagerComponent(
            nextButton = Button(10),
            beforeButton = Button(11),
            digitalEncoder = DigitalEncoder(1, 2, 3)
        )
