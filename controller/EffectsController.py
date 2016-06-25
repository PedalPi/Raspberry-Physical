# -*- coding: utf-8 -*-
from .AbstractConfigurationController import AbstractConfigurationController


class EffectsController(AbstractConfigurationController):

    def __init__(self, physical, patch):
        self.physical = physical
        self.patch = patch

        self.effectFocused = 0

    def onNext(self):
        if self.effectFocused == len(self.effects)-1:
            self.effectFocused = -1

        self.effectFocused += 1
        self.showEffect(self.effectFocused)
    
    def onBefore(self):
        if self.effectFocused == 0:
            self.effectFocused = len(self.effects)

        self.effectFocused -= 1
        self.showEffect(self.effectFocused)

    def onSelect(self):
        self.physical.toParamsController()

    def toggle(self):
        current = self.physical.currentActions
        current.toggleEffectStatus(self.effectFocused)

    @param
    def effects(self):
        return self.patch['effects']

    def showEffect(self, effectIndex):
        effect = self.effects[effectIndex]
        self.physical.display.showEffect(effect)
