# -*- coding: utf-8 -*-
from configurations import Configurations
from action.CurrentActions import CurrentActions


class Physical(object):
    config = None

    def __init__(self):
        self.app = Application()
        self.config = Configurations()

        if self.config.display:
            self.config.display.init()

        currentActions = CurrentActions(self.app)

        self.config.nextPatchButton.action = currentActions.toNextPatch
        self.config.beforePatchButton.action = currentActions.toBeforePatch

    def initControllers(self):
        self.effectController = EffectsController(self, patch)
        self.paramsController = Paramsontroller(self, patch)

    def setController(self, controller):
        manager = self.config.manager

        manager.onNext = controller.onNext
        manager.onBefore = controller.onBefore
        manager.onClick = controller.onClick

    def toEffectsController(self):
        self.setController(self.effectsController)

    def toParamsController(self):
        self.setController(self.paramsController)
