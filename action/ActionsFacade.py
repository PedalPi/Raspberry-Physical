from application.controller.CurrentController import CurrentController


class ActionsFacade(object):

    def __init__(self, application):
        self.app = application

    @property
    def currentPatch(self):
        controller = self.app.controller(CurrentController)
        return controller.currentPatch

    def toNextPatch(self):
        controller = self.app.controller(CurrentController)

        controller.toNextPatch()
        return controller.currentPatch

    def toBeforePatch(self):
        controller = self.app.controller(CurrentController)

        controller.toBeforePatch()
        return controller.currentPatch
