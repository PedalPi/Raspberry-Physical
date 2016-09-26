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
                    colors[x][y] = canvas.itemcget(index, "fill")
                    if colors[x][y] is None:
                        colors[x][y] = Color.WHITE
                        print("ImageUtils.getPixelsOf NONE INDEVIDO")
                    else:
                        colors[x][y] = Color.BLACK
                else:
                    colors[x][y] = Color.WHITE
                #print(str(x), str(y), "-", colors[x][y], end = "")

        return colors
        #canvas.pack(fill=BOTH, expand=1)
