# -*- coding: utf-8 -*-
from controller.Controller import Controller
from mvc.patches.PatchesView import PatchesView


class PatchesController(Controller):
    indexEffectFocused = 0

    def __init__(self, components, actions):
        self.__init__(components, actions, PatchesView)

    def init(self, currentPatch):
        self.view.showPatch(currentPatch)

    def toNextPatch(self):
        nextPatch = self.actions.toNextPatch()
        self.init(nextPatch)

    def toBeforePatch(self):
        beforePatch = self.actions.toBeforePatch()
        self.init(beforePatch)

    def toggleStatusEffect(self):
        beforePatch = self.actions.toBeforePatch()
        self.init(beforePatch)
