from base.View import View

from component.Components import Components


class PatchesView(View):
    controller = None

    display = None
    nextPatch = None
    beforePatch = None
    effect = None
    rotaryEncoder = None

    def init(self, controller):
        self.controller = controller

    def initComponents(self, components):
        self.display = components[Components.DISPLAY]

        self.nextPatch = components[Components.NEXT_PATCH]
        self.beforePatch = components[Components.BEFORE_PATCH]

        self.effect = components[Components.EFFECT]

        self.rotaryEncoder = components[Components.DIGITAL_ENCODER]

    def initComponentsActions(self):
        self.effect.action = self.controller.toggleStatusEffect

        self.nextPatch.action = self.controller.toNextPatch
        self.beforePatch.action = self.controller.toBeforePatch

        self.rotaryEncoder.when_rotated = self.when_rotary_rotated
        self.rotaryEncoder.when_selected = self.controller.toEffectsController

    def when_rotary_rotated(self, state):
        if state == 1:
            self.controller.toNextEffect()
        else:
            self.controller.toBeforeEffect()

    def showPatch(self, patch):
        print("Patch:", patch['name'])
        #self.display

    def showEffect(self, effect):
        print("Effect:", effect.index, "-", effect['uri'])
        self.display.showEffect(effect)
