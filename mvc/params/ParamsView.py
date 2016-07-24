from base.View import View

from component.Components import Components


class ParamsView(View):
    controller = None

    display = None
    nextPatch = None
    beforePatch = None
    effect = None
    rotaryEncoder = None

    def init(self, controller):
        print(controller)
        self.controller = controller

    def initComponents(self, components):
        self.display = components[Components.DISPLAY]

        self.nextPatch = components[Components.NEXT_PATCH]
        self.beforePatch = components[Components.BEFORE_PATCH]

        self.effect = components[Components.EFFECT]

        self.rotaryEncoder = components[Components.DIGITAL_ENCODER]

    def initComponentsActions(self):
        self.effect.action = self.controller.returnToParamsController

        self.nextPatch.action = self.controller.returnToParamsController
        self.beforePatch.action = self.controller.returnToParamsController

        self.rotaryEncoder.when_selected = self.controller.toNextParam
        self.rotaryEncoder.when_rotated = self.when_rotary_rotated

    def when_rotary_rotated(self, state):
        if state == 1:
            self.controller.addValue()
        else:
            self.controller.minusValue()

    def showParam(self, param):
        self.display.showParam(param)
