# -*- coding: utf-8 -*-
#http://zetcode.com/gui/tkinter/drawing/
#https://mail.python.org/pipermail/tutor/2012-November/092795.html

from util.color import Color

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

        draw.rectangle([(0, 0), (self.display.width, self.display.height)])
        self.display.clear()
        del draw

    def dispose(self):
        import time
        start_time1 = time.time()
        #self._draw_display()
        self._draw_display2()
        start_time2 = time.time()
        #self.display.redraw()

        print(" - Discover changes: %s seconds " % (time.time() - start_time1))
        print(" Redraw time: %s seconds " % (time.time() - start_time2))

    def _draw_display(self):
        """
        :param Color[][] pixels:
        """
        import time
        start_time1 = time.time()
        pixels = list(self.image.getdata())

        pixels = [pixels[i * self.display.width:(i + 1) * self.display.width] for i in range(self.display.height)]

        start_time2 = time.time()
        for y in range(self.display.height):
            for x in range(self.display.width):
                pixel = pixels[y][x]
                color = Color.WHITE if pixel == 0 else Color.BLACK
                self.display_buffer.set_pixel(x, y, color)
            '''
                if pixels[x][y] == Color.WHITE:
                    print(' ', end='')
                else:
                    print('.', end='')
            print()
            '''

        start_time3 = time.time()
        iterator = self.display_buffer.iterator

        while iterator.has_next():
            pixel = iterator.next_element()
            self.display.set_pixel(pixel.x, pixel.y, pixel.color)

        print("  - TOTAL: %s seconds " % (time.time() - start_time1))
        print("  - Analise changes")
        print("    - Only get pixels: %s seconds " % (start_time2 - start_time1))
        print("    - Only add buffer 1: %s seconds " % (start_time3 - start_time2))
        print("  - Mark changes: %s seconds " % (time.time() - start_time3))

    def _draw_display2(self):
        """
        :param Color[][] pixels:
        """
        from functools import reduce
        import numpy

        pixels = list(self.image.getdata())
        #pixels = [pixels[i * self.display.width:(i + 1) * self.display.width] for i in range(self.display.height)]
        #pixels = numpy.array(pixels)
        #pixels = pixels.T

        #pixels = reduce(lambda result, lista: result + lista, pixels, [])

        byte_size = 8

        pixels = [
            reduce(
                lambda byte, bit: int(byte << 1 | bit),
                pixels[i * byte_size:(i + 1) * byte_size]
            )
            for i in range(int((self.display.height*self.display.width)/byte_size))
        ]

        #print(pixels)

        self.display._send_data_bytes(0, 0, pixels)
        """
        print(pixels)

        for y in range(self.display.height):
            for x in range(self.display.width):
                pixel = pixels[y][x]
                color = Color.WHITE if pixel == 0 else Color.BLACK
                self.display.set_pixel(x, y, color)
            '''
                if pixels[x][y] == Color.WHITE:
                    print(' ', end='')
                else:
                    print('.', end='')
            print()
            '''
        """