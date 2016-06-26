# -*- coding: utf-8 -*-


class PixelBuffer:
    """
    Store in memory a pixel color state
    """
    x = 0
    y = 0
    color = None

    """"Color of the last change"""
    lastChangeColor = None

    def __init__(self, x, y, color):
        """
        :param int x
        :param int y
        :param Color color
        """
        self.x = x
        self.y = y
        self.color = color
        self.lastChangeColor = color

    def hasRealChange(self):
        return self.lastChangeColor != self.color

    def updateLastChangeColor(self, color):
        """
        :param Color color
        """
        self.lastChangeColor = color

    def __repr__(self):
        return "Pixel(x=" + str(self.x) + ", y=" + str(self.y) + ") - " + \
               self.color
