from application.controller.CurrentController import CurrentController
from application.controller.EffectController import EffectController


class ActionsFacade(object):

    def __init__(self, application):
        self.app = application

    @property
    def current_patch(self):
        controller = self.app.controller(CurrentController)
        return controller.currentPatch

    def to_next_patch(self):
        controller = self.app.controller(CurrentController)

        controller.toNextPatch()
        return controller.currentPatch

    def to_before_patch(self):
        controller = self.app.controller(CurrentController)

        controller.toBeforePatch()
        return controller.currentPatch

    def toggle_status_effect(self, effect):
        controller = self.app.controller(EffectController)
        controller.toggleStatus(effect)

    def set_param_value(self, param, new_value):
        effect = param.effect
        controller = self.app.controller(CurrentController)
        controller.setEffectParam(effect.index, param.index, new_value)
