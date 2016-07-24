from component.Display import Display
from component.androiddisplay.DisplayServer import DisplayServer


class AndroidDisplay(Display):
    server = None

    def __init__(self, host, port):
        self.server = DisplayServer()
        self.server.listen(port, host)

    def showEffect(self, effect):
        print(effect.index, '-', effect['name'])
        print(effect['uri'])

    def showParam(self, param):
        print(param.index, '-', param['name'])
        print(param.value, '(', param['ranges']['minimum'], '-', param['ranges']['maximum'], ')')
