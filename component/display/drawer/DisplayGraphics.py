# -*- coding: utf-8 -*-
#http://zetcode.com/gui/tkinter/drawing/
#https://mail.python.org/pipermail/tutor/2012-November/092795.html

from tkinter import Canvas

from util.Color import Color
from util.ImageUtils import ImageUtils

from drawer.buffer.DisplayBuffer import DisplayBuffer


class DisplayGraphics(object):
    """
    A Graphics implementation for any Display type
    """

    display = None

    canvas = None

    displayBuffer = None

    initialColor = None

    def __init__(self, display, initialColor):
        """
        :param Display display
        :param Color initialColor
        :param ColorType type
        """
        self.display = display
        self.canvas = Canvas(None, width=display.width, height=display.height, background=initialColor.value)
        self.displayBuffer = DisplayBuffer(display.width, display.height, initialColor)
        self.initialColor = initialColor

    def clear(self):
        self.canvas.create_rectangle(0, 0, 83, 47, fill=self.initialColor.value)
        self.display.clear()

    def dispose(self):
        pixels = ImageUtils.getPixelsOf(self.canvas)
        self._drawDisplay(pixels)
        self.display.redraw()

    def _drawDisplay(self, pixels):
        """
        :param Color[][] pixels:
        """
        width = len(pixels)
        height = len(pixels[0])

        for y in range(height):
            for x in range(width):
                self.displayBuffer.setPixel(x, y, pixels[x][y])
                if pixels[x][y] == Color.WHITE:
                    print(' ', end='')
                else:
                    print('.', end='')
            print()

        iterator = self.displayBuffer.iterator

        while iterator.hasNext():
            pixel = iterator.nextElement()
            self.display.setPixel(
                pixel.x,
                pixel.y,
                pixel.color
            )
