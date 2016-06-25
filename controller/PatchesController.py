# -*- coding: utf-8 -*-


class PatchesController(object):
    actions = None

    def __init__(self, physical):
        self.phyisical = phyisical
        self.actions = CurrentActions(physical.app)

    def nextPatch(self):
        self.actions.toNextPatch()

    def beforePatch(self):
        self.actions.toBeforePatch()

    def updateDisplay(self):
        display = self.physical.displayController
        currentPatch = self.actions.currentPatch()

        display.showPatch(currentPatch)
