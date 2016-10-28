# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod


class Controller(metaclass=ABCMeta):
    controllers = None
    components = None
    actions = None
    view = None

    def __init__(self, controllers, components, actions, observer, view):
        self.controllers = controllers
        self.components = components
        self.actions = actions
        self.observer = observer
        self.view = view()

    @abstractmethod
    def init(self):
        raise NotImplementedError()

    def start(self):
        self.view.init(self)
        self.view.init_components(self.components)
        self.view.init_components_actions()
        self.register()

    def register(self):
        self.observer.register(self)

    def on_current_patch_change(self, patch, token=None):
        pass

    def on_bank_update(self, bank, update_type, token=None):
        pass

    def on_patch_updated(self, patch, update_type, token=None):
        pass

    def on_effect_updated(self, effect, update_type, token=None):
        pass

    def on_effect_status_toggled(self, effect, token=None):
        pass

    def on_param_value_change(self, param, token=None):
        pass
