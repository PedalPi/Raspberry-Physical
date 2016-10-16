from physical.controller.pedal_zero_controller.component.display import Display


class DisplaysComponent(Display):

    def __init__(self):
        self.displays = []

    def append(self, display):
        self.displays.append(display)

    def show_param(self, param):
        for display in self.displays:
            display.show_param(param)

    def show_effect(self, effect):
        for display in self.displays:
            display.show_effect(effect)
