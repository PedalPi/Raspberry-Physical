# -*- coding: utf-8 -*-
from util.color import Color


class ImageUtils:

    @staticmethod
    def get_pixels_of(canvas):
        width = int(canvas["width"])
        height = int(canvas["height"])
        colors = []

        for x in range(width):
            column = []
            for y in range(height):
                column.append(ImageUtils.get_pixel_color(canvas, x, y))
            colors.append(column)

        return colors

    @staticmethod
    def get_pixel_color(canvas, x, y):
        ids = canvas.find_overlapping(x, y, x, y)

        if len(ids) > 0:
            index = ids[-1]
            color = canvas.itemcget(index, "fill")
            color = color.upper()
            if color != '':
                return Color[color.upper()]

        return Color.WHITE
