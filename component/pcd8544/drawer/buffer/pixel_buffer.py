# -*- coding: utf-8 -*-


class PixelBuffer:
    """
    Store in memory a pixel color state
    """

    def __init__(self, x, y, color):
        """
        :param int x:
        :param int y:
        :param Color color:
        """
        self.x = x
        self.y = y
        self.color = color
        self.last_change_color = color

    def has_real_change(self):
        return self.last_change_color != self.color

    def update_last_change_color(self):
        self.last_change_color = self.color

    def __repr__(self):
        return "Pixel(x=" + str(self.x) + ", y=" + str(self.y) + ") - " + \
               str(self.color)
