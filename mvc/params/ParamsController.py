# -*- coding: utf-8 -*-
from base.Controller import Controller
from mvc.params.ParamsView import ParamsView


class ParamsController(Controller):
    indexParamFocused = 0
    currentEffect = None

    def __init__(self, controllers, components, actions):
        super().__init__(controllers, components, actions, ParamsView)

    def init(self, currentEffect):
        self.currentEffect = currentEffect

        self.view.showParam(self.currentParam)

        print('=' * 25)
        print("Param:", self.currentParam['name'])
        print('=' * 25)

    def toNextParam(self):
        if self.indexParamFocused == len(self.params) - 1:
            self.indexParamFocused = -1

        self.indexParamFocused += 1
        self.view.showParam(self.currentParam)

    def addValue(self):
        param = self.currentParam

        maximum = param['ranges']['maximum']
        newValue = param.value + 1
        if newValue > maximum:
            newValue = maximum

        self.actions.set_param_value(param, newValue)
        self.view.showParam(param)

    def minusValue(self):
        param = self.currentParam

        minimum = param['ranges']['minimum']
        newValue = param.value - 1
        if newValue < minimum:
            newValue = minimum

        self.actions.set_param_value(param, newValue)
        self.view.showParam(param)

    @property
    def params(self):
        return self.currentEffect.params

    @property
    def currentParam(self):
        return self.params[self.indexParamFocused]

    def returnToParamsController(self):
        from mvc.patches.PatchesController import PatchesController

        controller = self.controllers[PatchesController]
        controller.start()
        controller.init(self.currentEffect.patch)
