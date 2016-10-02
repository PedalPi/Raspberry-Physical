from gpiozero import DigitalOutputDevice


class CommonStrategy(object):

    def __init__(self, display, common):
        self.display = display
        self.common = DigitalOutputDevice(common)

    def on(self):
        self.common.value = not self.display.anode

    def off(self):
        self.common.value = self.display.anode

    def rewrite(self):
        self.display._write(self.display.value)


class NotCommonStrategy(object):

    def __init__(self, display):
        self.display = display

    def on(self):
        self.rewrite()

    def off(self):
        self.rewrite()

    def rewrite(self):
        character = self.display.value if self.display.status else ' '

        self.display._write(character)
