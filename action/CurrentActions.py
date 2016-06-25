# -*- coding: utf-8 -*-
from application.controller.CurrentController import CurrentController


class CurrentActions(object):

    def __init__(self, application):
        self.app = application
        self.controller = self.app.controller(CurrentController)

    def toNextPatch(self):
        self.controller.toNextPatch()

    def toBeforePatch(self):
        self.controller.toBeforePatch()

    def toggleEffectStatus(self, effectIndex):
        self.controller.toggleStatusEffect(effectIndex)

    @param
    def currentPatch(self):
        return controller.getCurrentPatch()
