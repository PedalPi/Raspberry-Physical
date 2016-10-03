from base.View import View

from component.Components import Components


class PatchesView(View):
    controller = None

    display = None
    next_patch = None
    before_patch = None
    effect = None
    rotary_encoder = None

    def init(self, controller):
        self.controller = controller

    def init_components(self, components):
        self.display = components[Components.DISPLAY]

        self.next_patch = components[Components.NEXT_PATCH]
        self.before_patch = components[Components.BEFORE_PATCH]

        self.effect = components[Components.EFFECT]

        self.rotary_encoder = components[Components.DIGITAL_ENCODER]

    def init_components_actions(self):
        self.effect.action = self.controller.toggle_status_effect

        self.next_patch.action = self.controller.to_next_patch
        self.before_patch.action = self.controller.to_before_patch

        self.rotary_encoder.when_rotated = self.when_rotary_rotated
        self.rotary_encoder.when_selected = self.controller.to_effects_controller

    def when_rotary_rotated(self, state):
        if state == 1:
            self.controller.to_next_nffect()
        else:
            self.controller.to_before_effect()

    def show_effect(self, effect):
        self.display.show_effect(effect)
