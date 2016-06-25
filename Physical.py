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

        #self.config.effects[0].action = currentActions.setEffectParam
