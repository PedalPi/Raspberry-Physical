# -*- coding: utf-8 -*-


class ImageUtils:

    @staticmethod
    def getPixelsOf(canvas):
        colors = [[None] * 80] * 80

        for y in range(40):
            for x in range(40):
                ids = canvas.find_overlapping(x, y, x, y)

                if len(ids) > 0:
                    index = ids[-1]
                    colors[x][y] = colors.append(canvas.itemcget(index, "fill"))

        return colors
        #canvas.pack(fill=BOTH, expand=1)
