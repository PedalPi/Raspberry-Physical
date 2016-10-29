# -*- coding: utf-8 -*-
from functools import reduce
import numpy

from PIL import Image, ImageDraw


class DisplayGraphics(object):

    """
    A Graphics implementation for any Display type usign Pillow
    """
    def __init__(self, display):
        """
        :param Display display:
        """
        self.display = display
        self.image = Image.new('1', (display.width, display.height))

        self.draw = ImageDraw.Draw(self.image)

    def clear(self):
        self.draw.rectangle([(0, 0), (self.display.width, self.display.height)], fill=0)

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

        print(" - Discover changes: %s seconds " % (time.time() - start_time1))

    def close(self):
        del self.draw
        del self.image

    def open(self, image):
        self.close()

        self.image = Image.open(image) \
            .crop((0, 0, self.display.width, self.display.height)) \
            .convert("1", colors=2)
            #.resize((self.display.width, self.display.height)) \

        self.draw = ImageDraw.Draw(self.image)
