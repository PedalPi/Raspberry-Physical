from abc import ABCMeta, abstractmethod


class Controller(metaclass=ABCMeta):

    def __init__(self, controllers, components, actions, observer, view):
        self.controllers = controllers
        self.components = components
        self.actions = actions
        self.observer = observer
        self.view = view()

    @abstractmethod
    def init(self, *args, **kwargs):
        raise NotImplementedError()

    def start(self):
        self.view.init(self)
        self.view.init_components(self.components)
        self.view.init_components_actions()
        self.register()

    def register(self):
        self.observer.register(self)
