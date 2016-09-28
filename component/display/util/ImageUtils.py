# -*- coding: utf-8 -*-
from util.Color import Color


class ImageUtils:

    @staticmethod
    def getPixelsOf(canvas):
        width = int(canvas["width"])
        height = int(canvas["height"])
        colors = []

        for x in range(width):
            column = []
            for y in range(height):
                column.append(ImageUtils.getColorOfPixel(canvas, x, y))
            colors.append(column)

        return colors

    @staticmethod
    def getColorOfPixel(canvas, x, y):
        ids = canvas.find_overlapping(x, y, x, y)

        if len(ids) > 0:
            index = ids[-1]
            color = canvas.itemcget(index, "fill")
            color = color.upper()
            if color != '':
                return Color[color.upper()]

        return Color.WHITE
