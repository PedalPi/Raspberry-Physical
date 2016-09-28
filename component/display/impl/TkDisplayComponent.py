# -*- coding: utf-8 -*-

from time import sleep

from tkinter import Tk, Frame

from Display import Display
from drawer.buffer.PixelBuffer import PixelBuffer

from util.Color import Color


class TkDisplayComponent(Display):
    """
    Based in Erkki 22-Jul-2014
    https://raw.githubusercontent.com/noxo/SnakePI4J/master/src/org/noxo/devices/AWTDisplay.java

    WARNING: This don't works in Raspberry Pi - Console mode.
    Use for visual interfaces tests :D
    """
    screen = None
    width = 0
    height = 0

    changesBuffer = None
    debugMode = False

    def __init__(self, width, height, debugMode=False):
        """
        :param int width
        :param int height
        :param bool debugMode
        """
        self.width = width
        self.height = height

        self.debugMode = debugMode

        self.changesBuffer = []

        tk = Tk()
        screen = Frame(tk, width=width, height=height)
        tk.mainloop()
        #screen.setUndecorated(True)
        #screen.validate()
        #screen.setVisible(True)

    def setPixel(self, x, y, color):
        """
        :param int x
        :param int y
        :param Color color
        """
        self.changesBuffer.add(PixelBuffer(x, y, color))

    def redraw(self):
        img = BufferedImage(width, height, BufferedImage.TYPE_INT_ARGB);

        while not self.changesBuffer.isEmpty():
            pixel = self.changesBuffer.remove()
            img.setRGB(pixel.x, pixel.y, pixel.getColor().getRGB())

            if debugMode:
                self._simulateGPIODelay()

            g = self.screen.getGraphics()
            g.drawImage(img, 0, 0, screen)

    def _simulateGPIODelay(self):
        sleep(0)

    def clear(self):
        self.changesBuffer.clear()

        for x in range(self.width):
            for y in range(self.height):
                self.changesBuffer.append(PixelBuffer(x, y, Color.WHITE))
