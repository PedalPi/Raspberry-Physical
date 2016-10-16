from abc import ABCMeta


class Display(metaclass=ABCMeta):

    def show_effect(self, effect):
        raise NotImplementedError()

    def show_param(self, param):
        raise NotImplementedError()
