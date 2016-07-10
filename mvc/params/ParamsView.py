from base.View import View

from component.Components import Components


class ParamsView(View):
    controller = None

    display = None
    digitalEncoder = None

    def init(self, controller):
        self.controller = controller

    def initComponents(self, components):
        self.display = components[Components.DISPLAY]
        self.digitalEncoder = components[Components.DIGITAL_ENCODER]

    def initComponentsActions(self):
        self.digitalEncoder.minusAction = self.controller.addValue
        self.digitalEncoder.plusAction = self.controller.minusValue

        self.digitalEncoder.selectAction = self.controller.toNextParam

    def showEffect(self, effect):
        print("Effect:", effect['uri'])
        #self.display

    def showParam(self, param):
        print("Param:", param['name'])
        #self.display
