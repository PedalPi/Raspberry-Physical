# -*- coding: utf-8 -*-
from collections import deque

from util.privatemethod import privatemethod
from drawer.buffer.PixelBuffer import PixelBuffer


class DisplayBuffer(object):
    """
    DisplayBuffer its a good auto dettecter changes.


    Change the required pixels and - for update the
    real component display - calls getChanges() method.</p>

    This will only return the pixel that has actually changed,
    avoiding unnecessary updates.

    This buffer is used in DisplayGraphics.
    Consequently, all of it coming changes will be ONLY the pixels changed by it

    In its Display implementations, it's necessary only to have
    a queue of updated pixels, where each pixel is inserted into
    "display.setPixel()". And in "display.redraw()", it is only
    necessary to read this queue and update the display based on
    this row.

    Find class AWTDisplayComponent for an example.

    But, if a byte represents more than one color,
    you can create a special buffer implementation in these cases.
    Find class PCB8544DisplayDataRam for inspiration!
    """
    changes = deque()

    dataBuffer = None

    width = 0
    height = 0
    defaultColor = 0

    def __init__(self, width, height, defaultColor):
        """
       :param int width: Total columns
       :param int height: Total rows
       :param Color defaultColor: Initializes the pixels with this color
                           (in the initial state, is assumed that all the
                            pixels are in the currentColor)
        """
        self.width = width
        self.height = height
        self.dataBuffer = [[None] * height] * width
        self.defaultColor = defaultColor

    def setPixel(self, x, y, color):
        """
        Set a specific pixel for a color

        :param int x: Row position. 0 is first, top to down direction
        :param int y: Column position. 0 is first, left to right direction
        :param Color color
        """
        pixel = self.getPixel(x, y)

        if pixel is None:
            return  # or throws?

        elif pixel.color == color:
            return

        pixel.color = color
        self.changes.append(pixel)

    @privatemethod
    def getPixel(self, x, y):
        """
        :param int x
        :param int y
        """
        if x < 0 or x > self.width - 1 \
        or y < 0 or y > self.height - 1:
            return None

        pixel = self.dataBuffer[x][y]
        if pixel is None:
            pixel = PixelBuffer(x, y, self.defaultColor)
            self.dataBuffer[x][y] = pixel

        return pixel

    def getChanges(self):
        """
        CAUTION
        For any iterator.hasNext(), the element returned
        should be removed in the changes queue

        :return Iterator: All changes detected
        """
        return self.iterator

    @property
    def iterator(self):
        return DisplayBufferIterator(self.changes)


class DisplayBufferIterator(object):
    changes = None

    _nextElement = None

    def __init__(self, changes):
        """
        :param deque<PixelBuffer> changes
        """
        self.changes = changes

    def hasNext(self):
        self._nextElement = self.findNext()
        return self._nextElement is not None

    @privatemethod
    def findNext(self):
        if len(self.changes) == 0:
            pixelBuffer = None
        else:
            pixelBuffer = self.changes.popleft()

        while pixelBuffer is not None and not pixelBuffer.hasRealChange():
            pass

        return pixelBuffer

    def nextElement(self):
        pixelBuffer = self._nextElement
        pixelBuffer.updateLastChangeColor()

        return pixelBuffer
