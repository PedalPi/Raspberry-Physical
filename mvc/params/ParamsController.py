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

        self.view.showEffect(currentEffect)
        self.view.showParam(self.currentParam)

    def toNextParam(self):
        if self.indexParamFocused == len(self.params) - 1:
            self.indexParamFocused = -1

        self.indexParamFocused += 1
        self.view.showParam(self.currentParam)

    def addValue(self):
        print("value is += 1")
        self.view.showParam(self.currentParam)

    def minusValue(self):
        print("value is -= 1")
        self.view.showParam(self.currentParam)

    @property
    def params(self):
        return self.currentEffect.params

    @property
    def currentParam(self):
        return self.params[self.indexParamFocused]
