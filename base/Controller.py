# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod


class Controller(metaclass=ABCMeta):
    controllers = None
    components = None
    actions = None
    view = None

    def __init__(self, controllers, components, actions, view):
        self.controllers = controllers
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
