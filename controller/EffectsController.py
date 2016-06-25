# -*- coding: utf-8 -*-
from .AbstractConfigurationController import AbstractConfigurationController


class EffectsController(AbstractConfigurationController):

    def __init__(self, physical, patch):
        self.physical = physical
        self.patch = patch

    def onNext(self):
        pass
    
    def onBefore(self):
        pass

    def onSelect(self):
        self.physical.toParamsController()
