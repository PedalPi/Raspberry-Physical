from abc import ABCMeta


class Display(metaclass=ABCMeta):

    def showEffect(self, effect):
        pass

    def showParam(self, param):
        pass
