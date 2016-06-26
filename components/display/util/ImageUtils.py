# -*- coding: utf-8 -*-
from util.Color import Color


class ImageUtils:

    @staticmethod
    def getPixelsOf(canvas):
        width = int(canvas["width"])
        height = int(canvas["height"])
        colors = [[None] * height] * width

        for y in range(height):
            for x in range(width):
                ids = canvas.find_overlapping(x, y, x, y)

                if len(ids) > 0:
                    index = ids[-1]
                    colors[x][y] = colors.append(canvas.itemcget(index, "fill"))
                else:
                    colors[x][y] = Color.WHITE
                print(str(x), str(y), "-", colors[x][y])

        return colors
        #canvas.pack(fill=BOTH, expand=1)
