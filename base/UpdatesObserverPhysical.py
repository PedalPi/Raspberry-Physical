from application.model.UpdatesObserver import UpdatesObserver
from physical.action.ActionsFacade import ActionsFacade


class UpdatesObserverPhysical(UpdatesObserver):

    def __init__(self):
        self.controller = None

    def register(self, controller):
        self.controller = controller

    def onCurrentPatchChange(self, patch, token=None):
        if self.controller is not None \
        and token != ActionsFacade.TOKEN:
            self.controller.on_current_patch_change(patch, token)

    def onBankUpdate(self, bank, update_type, token=None):
        if self.controller is not None \
        and token != ActionsFacade.TOKEN:
            self.controller.on_bank_update(bank, update_type, token)

    def onPatchUpdated(self, patch, update_type, token=None):
        if self.controller is not None \
        and token != ActionsFacade.TOKEN:
            self.controller.on_patch_updated(patch, update_type, token)

    def onEffectUpdated(self, effect, update_type, token=None):
        if self.controller is not None \
        and token != ActionsFacade.TOKEN:
            self.controller.on_effect_updated(effect, update_type, token)

    def onEffectStatusToggled(self, effect, token=None):
        if self.controller is not None \
        and token != ActionsFacade.TOKEN:
            self.controller.on_effect_status_toggled(effect, token)

    def onParamValueChange(self, param, token=None):
        if self.controller is not None \
        and token != ActionsFacade.TOKEN:
            self.controller.on_param_value_change(param, token)
