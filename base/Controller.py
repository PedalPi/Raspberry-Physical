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

    @abstractmethod
    def init(self):
        pass

    def start(self):
        self.view.init(self)
        self.view.initComponents(self.components)
        self.view.initComponentsActions()
