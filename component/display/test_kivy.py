from kivy.app import App
from kivy.lang import Builder

from kivy.core.window import Window

Window.size = (320, 240)
Window.clearcolor = (236/255, 240/255, 241/255, 1)


class PedalPiDisplayApp(App):
    icon = 'icon.png'
    title = 'Pedal Pi'

    def build(self):
        self.root = Builder.load_file('layout.kv')
        return self.root

if __name__ == "__main__":
    PedalPiDisplayApp().run()
