from abc import ABCMeta, abstractmethod


class View(metaclass=ABCMeta):

    @abstractmethod
    def init(self, controller):
        raise NotImplementedError()

    @abstractmethod
    def init_components(self, components):
        raise NotImplementedError()

    @abstractmethod
    def init_components_actions(self):
        raise NotImplementedError()
