from base.View import View

from component.Components import Components


class PatchesView(View):
    controller = None

    display = None
    nextPatch = None
    beforePatch = None
    effect = None
    digitalEncoder = None

    def init(self, controller):
        self.controller = controller

    def initComponents(self, components):
        self.display = components[Components.DISPLAY]

        self.nextPatch = components[Components.NEXT_PATCH]
        self.beforePatch = components[Components.BEFORE_PATCH]

        self.effect = components[Components.EFFECT]

        self.digitalEncoder = components[Components.DIGITAL_ENCODER]

    def initComponentsActions(self):
        self.effect.action = self.controller.toggleStatusEffect

        self.nextPatch.action = self.controller.toNextPatch
        self.beforePatch.action = self.controller.toBeforePatch

        self.digitalEncoder.minusAction = self.controller.toNextEffect
        self.digitalEncoder.plusAction = self.controller.toBeforeEffect

        self.digitalEncoder.selectAction = self.controller.toEffectsController

    def showPatch(self, patch):
        print("Patch:", patch['name'])
        #self.display

    def showEffect(self, effect):
        print("Effect:", effect['uri'])
        #self.display
