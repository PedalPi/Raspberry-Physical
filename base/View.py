# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod


class View(metaclass=ABCMeta):

    @abstractmethod
    def init(self, controller):
        pass

    @abstractmethod
    def initComponents(self, components):
        pass

    @abstractmethod
    def initComponentsActions(self):
        pass
