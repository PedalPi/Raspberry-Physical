from base.View import View

from component.components import Components


class ParamsView(View):
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
        self.effect.action = self.controller.return_to_params_controller

        self.next_patch.action = self.controller.return_to_params_controller
        self.before_patch.action = self.controller.return_to_params_controller

        self.rotary_encoder.when_selected = self.controller.to_next_param
        self.rotary_encoder.when_rotated = self.when_rotary_rotated

    def when_rotary_rotated(self, state):
        if state == 1:
            self.controller.addValue()
        else:
            self.controller.minusValue()

    def show_param(self, param):
        self.display.showParam(param)
