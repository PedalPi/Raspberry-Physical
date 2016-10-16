# -*- coding: utf-8 -*-
from physical.controller.pedal_zero_controller.mvc.controller import Controller
from physical.controller.pedal_zero_controller.mvc.patches.patches_view import PatchesView


class PatchesController(Controller):
    index_effect_focused = 0
    current_patch = None

    def __init__(self, controllers, components, actions, observer):
        super().__init__(controllers, components, actions, observer, PatchesView)

    def init(self, current_patch):
        self.current_patch = current_patch
        self.view.show_effect(self.current_effect)

    def on_current_patch_change(self, patch, token=None):
        self.init(patch)

    def to_next_patch(self):
        next_patch = self.actions.to_next_patch()
        self.init(next_patch)

    def to_before_patch(self):
        before_patch = self.actions.to_before_patch()
        self.init(before_patch)

    def toggle_status_effect(self):
        effect = self.current_effect
        if effect is None:
            return

        print("Effect:", effect['uri'])
        print(" - Index:", self.index_effect_focused)
        print(" - Old status:", effect.status)
        self.actions.toggle_status_effect(effect)
        print(" - New status:", effect.status)

    @property
    def current_effect(self):
        if not self.current_patch.effects:
            return None

        return self.current_patch.effects[self.index_effect_focused]

    def to_next_effect(self):
        self.index_effect_focused += 1
        if self.index_effect_focused == len(self.current_patch.effects):
            self.index_effect_focused = 0

        self.view.showEffect(self.current_effect)

    def to_before_effect(self):
        self.index_effect_focused -= 1

        if self.index_effect_focused == -1:
            self.index_effect_focused = len(self.current_patch.effects) - 1

        self.view.showEffect(self.current_effect)

    def to_effects_controller(self):
        if self.current_effect is None:
            return

        from mvc.params.ParamsController import ParamsController

        controller = self.controllers[ParamsController]
        controller.start()
        controller.init(self.current_effect)
