# -*- coding: utf-8 -*-
#http://zetcode.com/gui/tkinter/drawing/
#https://mail.python.org/pipermail/tutor/2012-November/092795.html

from functools import reduce
import numpy

from drawer.buffer.display_buffer import DisplayBuffer
from PIL import Image, ImageDraw

class DisplayGraphicsPil(object):
    """
    A Graphics implementation for any Display type usign Pillow
    """
    def __init__(self, display, initial_color):
        """
        :param Display display:
        :param Color initial_color:
        """
        self.display = display
        self.image = Image.new('1', (display.width, display.height))

        self.display_buffer = DisplayBuffer(display.width, display.height, initial_color)
        self.initial_color = initial_color

    def clear(self):
        draw = ImageDraw.Draw(self.image)

        draw.rectangle([(0, 0), (self.display.width, self.display.height)], fill=0)
        self.display.clear()
        del draw

    def dispose(self):
        import time
        start_time1 = time.time()

        pixels = list(self.image.getdata())
        pixels = [pixels[i * self.display.width:(i + 1) * self.display.width] for i in range(self.display.height)]
        pixels_traspose = numpy.array(pixels).T

        concat = lambda result, lista: list(result) + list(lista)
        bits_to_byte = lambda byte, bit: int(byte << 1 | bit)

        pixels = reduce(concat, pixels_traspose, [])

        byte_size = 8

        pixels = [
            reduce(
                bits_to_byte,
                reversed(pixels[i * byte_size:(i + 1) * byte_size])
            )
            for i in range(int((self.display.height * self.display.width) / byte_size))
        ]

        self.display.write_all(pixels)

        start_time2 = time.time()

        print(" - Discover changes: %s seconds " % (time.time() - start_time1))
        print(" Redraw time: %s seconds " % (time.time() - start_time2))
