# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod


class Controller(metaclass=ABCMeta):
    view = None
    components = None
    actions = None

    def __init__(self, components, actions, view):
        self.components = components
        self.actions = actions
        self.view = view()

        self.initController(self.view)

    @abstractmethod
    def init(self):
        pass

    def initController(self, view):
        view.init(self)
        view.initComponents(self.components)
        view.initComponentsActions()

    def toController(self, controller, params):
        pass
