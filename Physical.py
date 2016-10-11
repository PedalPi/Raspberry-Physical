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

    def __init__(self, application, test=False):
        self.app = application
        self.config = Configurations(test=test)

        self.components = self.init_components(self.config)

        self.actions = ActionsFacade(application)
        self.controllers = self.init_controllers(self.components, self.actions)

        controller = self.controllers[PatchesController]
        controller.start()
        controller.init(self.actions.current_patch)

    def init_components(self, configurations):
        components = dict()

        components[Components.DISPLAY] = configurations.displays[0]
        components[Components.NEXT_PATCH] = configurations.next_patch_button
        components[Components.BEFORE_PATCH] = configurations.before_patch_button
        components[Components.EFFECT] = configurations.effect_button
        components[Components.DIGITAL_ENCODER] = configurations.rotary_encoder

        return components

    def init_controllers(self, components, actions):
        controllers = {}

        controllers[PatchesController] = PatchesController(controllers, components, actions)
        controllers[ParamsController] = ParamsController(controllers, components, actions)

        return controllers
