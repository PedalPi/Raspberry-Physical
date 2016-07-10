from base.View import View

from component.Components import Components


class PatchesView(View):
    controller = None

    def init(self, controller):
        self.controller = controller

    def initComponents(self, components):
        self.display = components[Components.DISPLAY]

        self.nextPatch = components[Components.NEXT_PATCH]
        self.beforePatch = components[Components.BEFORE_PATCH]

        self.effect = components[Components.EFFECT]

        self.digitalEncoder = components[Components.DIGITAL_ENCODER]

    def initComponentsActions(self):
        self.effect = ?
        self.nextPatch.action = self.controller.toNextPatch
        self.beforePatch.action = self.controller.toBeforePatch

        #self.digitalEncoder. ... = self.controller.toNextEffect
        #self.digitalEncoder. ... = self.controller.toBeforeEffect

    def showPatch(self, patch):
        print(patch)
        #self.display
        pass
