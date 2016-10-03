# -*- coding: utf-8 -*-
from application.controller.CurrentController import CurrentController


class CurrentActions(object):

    def __init__(self, application):
        self.app = application
        self.controller = self.app.controller(CurrentController)

    def to_next_patch(self):
        self.controller.toNextPatch()

    def to_before_patch(self):
        self.controller.toBeforePatch()

    def toggle_effect_status(self, effect_index):
        self.controller.toggleStatusEffect(effect_index)

    @property
    def current_patch(self):
        return self.controller.getCurrentPatch()
