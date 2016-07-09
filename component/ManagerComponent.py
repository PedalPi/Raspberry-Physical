# -*- coding: utf-8 -*-
from components.Components import Components


class ManagerComponent(object):
    components = None

    def __init__(self, configuration):
        self.components = dict()

        self.components[Components.DISPLAY] = configuration.display
        self.components[Components.NEXT_PATCH] = configuration.nextPatchButton
        self.components[Components.BEFORE_PATCH] = configuration.beforePatchButton
        self.components[Components.DIGITAL_ENCODER] = configuration.digitalEncoder
