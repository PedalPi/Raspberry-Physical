# -*- coding: utf-8 -*-
from physical.controller.pedal_zero_controller.configurations import Configurations
from physical.controller.pedal_zero_controller.component.components import Components
from physical.controller.pedal_zero_controller.action.actions_facade import ActionsFacade

from physical.controller.pedal_zero_controller.mvc.updates_observer_physical import UpdatesObserverPhysical
from physical.controller.pedal_zero_controller.mvc.params.params_controller import ParamsController
from physical.controller.pedal_zero_controller.mvc.patches.patches_controller import PatchesController

from physical.base.controller import Controller


class PedalZeroController(Controller):

    app = None
    config = None
    components = None
    observer = None
    controllers = None
    actions = None

    def __init__(self, application, test=False):
        super(PedalZeroController, self).__init__(application, self.__class__.__name__)

        self.app = application
        self.config = Configurations(test=test)

        self.components = self.init_components(self.config)
        self.observer = UpdatesObserverPhysical()
        self.register_observer(self.observer)

        self.actions = ActionsFacade(application)

        self.controllers = self.init_controllers(self.components, self.actions, self.observer)

    def init(self):
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
