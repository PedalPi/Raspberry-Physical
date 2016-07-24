# -*- coding: utf-8 -*-
from base.Controller import Controller
from mvc.patches.PatchesView import PatchesView


class PatchesController(Controller):
    indexEffectFocused = 0
    currentPatch = None

    def __init__(self, controllers, components, actions):
        super().__init__(controllers, components, actions, PatchesView)

    def init(self, currentPatch):
        self.currentPatch = currentPatch
        self.view.showEffect(self.currentEffect)

        print('=' * 25)
        print("Patch:", currentPatch['name'])
        print('=' * 25)

    def toNextPatch(self):
        nextPatch = self.actions.toNextPatch()
        self.init(nextPatch)

    def toBeforePatch(self):
        beforePatch = self.actions.toBeforePatch()
        self.init(beforePatch)

    def toggleStatusEffect(self):
        effect = self.currentEffect
        print("Effect:", effect['uri'])
        print(" - Index:", self.indexEffectFocused)
        print(" - Old status:", effect.status)
        self.actions.toggleStatusEffect(effect)
        print(" - New status:", effect.status)

    @property
    def currentEffect(self):
        return self.currentPatch.effects[self.indexEffectFocused]

    def toNextEffect(self):
        self.indexEffectFocused += 1
        if self.indexEffectFocused == len(self.currentPatch.effects):
            self.indexEffectFocused = 0

        self.view.showEffect(self.currentEffect)

    def toBeforeEffect(self):
        self.indexEffectFocused -= 1

        if self.indexEffectFocused == -1:
            self.indexEffectFocused = len(self.currentPatch.effects) - 1

        self.view.showEffect(self.currentEffect)

    def toEffectsController(self):
        from mvc.params.ParamsController import ParamsController

        controller = self.controllers[ParamsController]
        controller.start()
        controller.init(self.currentEffect)
