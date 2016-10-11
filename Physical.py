# -*- coding: utf-8 -*-
from configurations import Configurations

from action.ActionsFacade import ActionsFacade
from component.Components import Components

from mvc.params.ParamsController import ParamsController
from mvc.patches.PatchesController import PatchesController


class Physical(object):
    app = None
    config = None
    components = None
    controllers = None
    actions = None

    def __init__(self, application):
        self.app = application
        self.config = Configurations()

        self.components = self.init_components(self.config)

        self.actions = ActionsFacade(application)
        self.controllers = self.init_controllers(self.components, self.actions)

        controller = self.controllers[PatchesController]
        controller.start()
        controller.init(self.actions.currentPatch)

    def init_components(self, configurations):
        components = dict()

        components[Components.DISPLAY] = configurations.display
        components[Components.NEXT_PATCH] = configurations.nextPatchButton
        components[Components.BEFORE_PATCH] = configurations.beforePatchButton
        components[Components.EFFECT] = configurations.effectButton
        components[Components.DIGITAL_ENCODER] = configurations.digitalEncoder

        return components

    def init_controllers(self, components, actions):
        controllers = {}

        controllers[PatchesController] = PatchesController(controllers, components, actions)
        controllers[ParamsController] = ParamsController(controllers, components, actions)

        return controllers
