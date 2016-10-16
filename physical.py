# -*- coding: utf-8 -*-
from configurations import Configurations

from base.UpdatesObserverPhysical import UpdatesObserverPhysical

from action.ActionsFacade import ActionsFacade
from component.components import Components

from mvc.params.ParamsController import ParamsController
from mvc.patches.PatchesController import PatchesController


class Physical(object):

    app = None
    config = None
    components = None
    observer = None
    controllers = None
    actions = None

    def __init__(self, application, test=False):
        self.app = application
        self.config = Configurations(test=test)

        self.components = self.init_components(self.config)
        self.observer = UpdatesObserverPhysical()

        self.actions = ActionsFacade(application)
        self.actions.register(self.observer)

        self.controllers = self.init_controllers(self.components, self.actions, self.observer)

        controller = self.controllers[PatchesController]
        controller.start()
        controller.init(self.actions.current_patch)

    def init_components(self, configurations):
        components = dict()

        components[Components.DISPLAYS] = configurations.displays
        components[Components.NEXT_PATCH] = configurations.next_patch_button
        components[Components.BEFORE_PATCH] = configurations.before_patch_button
        components[Components.EFFECT] = configurations.effect_button
        components[Components.DIGITAL_ENCODER] = configurations.rotary_encoder

        return components

    def init_controllers(self, components, actions, observer):
        controllers = {}

        controllers[PatchesController] = PatchesController(controllers, components, actions, observer)
        controllers[ParamsController] = ParamsController(controllers, components, actions, observer)

        return controllers
