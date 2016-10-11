# -*- coding: utf-8 -*-
#http://zetcode.com/gui/tkinter/drawing/
#https://mail.python.org/pipermail/tutor/2012-November/092795.html

from tkinter import Canvas

from util.ImageUtils import ImageUtils

from drawer.buffer.DisplayBuffer import DisplayBuffer


class DisplayGraphics(object):
    """
    A Graphics implementation for any Display type
    """

    display = None

    canvas = None

    display_buffer = None

    initial_color = None

    def __init__(self, display, initial_color):
        """
        :param Display display:
        :param Color initial_color:
        """
        self.display = display
        self.canvas = Canvas(None, width=display.width, height=display.height, background=initial_color.value)
        self.display_buffer = DisplayBuffer(display.width, display.height, initial_color)
        self.initial_color = initial_color

    def clear(self):
        self.canvas.create_rectangle(0, 0, 83, 47, fill=self.initial_color.value)
        self.display.clear()

    def dispose(self):
        pixels = ImageUtils.get_pixels_of(self.canvas)
        #self._draw_display(pixels)
        self.display.redraw_test(pixels)

    def _draw_display(self, pixels):
        """
        :param Color[][] pixels:
        """
        width = len(pixels)
        height = len(pixels[0])

        for y in range(height):
            for x in range(width):
                self.display_buffer.set_pixel(x, y, pixels[x][y])
            '''
                if pixels[x][y] == Color.WHITE:
                    print(' ', end='')
                else:
                    print('.', end='')
            print()
            '''

        iterator = self.display_buffer.iterator

        while iterator.has_next():
            pixel = iterator.next_element()
            self.display.set_pixel(
                pixel.x,
                pixel.y,
                pixel.color
            )
