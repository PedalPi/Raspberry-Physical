from application.model.UpdatesObserver import UpdatesObserver
from application.controller.NotificationController import NotificationController


class ExternController(object):

    def __init__(self, application, token):
        """
        :param Application application:
        :param string token:
        """
        self.application = application
        self.token = token

    def controller(self, controller):
        return self.application.controller(controller)

    def register_observer(self, observer):
        """
        :param UpdatesObserver observer:
        """
        self.controller(NotificationController).register(observer)

    def unregister_observer(self, observer):
        self.controller(NotificationController).unregister(observer)
