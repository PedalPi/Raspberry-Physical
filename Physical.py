# -*- coding: utf-8 -*-
from configurations import Configurations


class Physical(object):
    config = None

    def __init__(self):
        self.app = Application()
        self.config = Configurations()

        self.initControllers()
        self.initActions()
        self.initComponents()

        self.patchesController.updateDisplay()

    def initControllers(self):
        self.displayController = DisplayController(self.config.display)

        self.patchesController = PatchesController(self, self)
        self.effectsController = EffectsController(self, patch)
        self.paramsController = ParamsController(self)

    def initComponents(self):
        if self.config.display:
            self.config.display.init()

        self.config.nextPatchButton.action = self.patchesController.nextPatch
        self.config.beforePatchButton.action = self.patchesController.beforePatch

        self.effectButton.action = self.config.effectsController.toggle

    def setController(self, controller):
        manager = self.config.manager

        manager.onNext = controller.onNext
        manager.onBefore = controller.onBefore
        manager.onClick = controller.onClick

    def toEffectsController(self):
        self.setController(self.effectsController)

    def toParamsController(self):
        self.setController(self.paramsController)
