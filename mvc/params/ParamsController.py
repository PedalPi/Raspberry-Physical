# -*- coding: utf-8 -*-
from base.Controller import Controller
from mvc.params.ParamsView import ParamsView


class ParamsController(Controller):
    index_param_focused = 0
    current_effect = None

    def __init__(self, controllers, components, actions):
        super().__init__(controllers, components, actions, ParamsView)

    def init(self, current_effect):
        self.current_effect = current_effect

        self.view.showParam(self.current_param)

        print('=' * 25)
        print("Param:", self.currentParam['name'])
        print('=' * 25)

    def to_next_param(self):
        if self.index_param_focused == len(self.params) - 1:
            self.index_param_focused = -1

        self.index_param_focused += 1
        self.view.showParam(self.current_param)

    def add_value(self):
        param = self.currentParam

        maximum = param['ranges']['maximum']
        new_value = param.value + 1
        if new_value > maximum:
            new_value = maximum

        self.actions.set_param_value(param, new_value)
        self.view.showParam(param)

    def minus_value(self):
        param = self.currentParam

        minimum = param['ranges']['minimum']
        new_value = param.value - 1
        if new_value < minimum:
            new_value = minimum

        self.actions.set_param_value(param, new_value)
        self.view.showParam(param)

    @property
    def params(self):
        return self.currentEffect.params

    @property
    def current_param(self):
        return self.params[self.index_param_focused]

    def return_to_params_controller(self):
        from mvc.patches.PatchesController import PatchesController

        controller = self.controllers[PatchesController]
        controller.start()
        controller.init(self.currentEffect.patch)
