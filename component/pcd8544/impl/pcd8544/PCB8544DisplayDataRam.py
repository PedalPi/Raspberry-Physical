# -*- coding: utf-8 -*-
from collections import deque

from MonochomaticDisplay import MonochomaticDisplay
from impl.pcd8544.PCD8544Constants import DisplaySize
from impl.pcd8544.PCB8544DDRamBank import PCB8544DDRamBank


class DisplayDataRamSize(object):
    DDRAM_WIDTH  = DisplaySize.WIDTH
    DDRAM_HEIGHT = int(DisplaySize.HEIGHT / 8)
    DDRAM_SIZE   = DDRAM_WIDTH * DDRAM_HEIGHT


class PCB8544DisplayDataRam(object):
    """
    Display Data Ram abstraction <br />
    See Pcd8544 datasheet for more information.
    """

    dataBuffer = [[None] * DisplayDataRamSize.DDRAM_HEIGHT for _ in range(DisplayDataRamSize.DDRAM_WIDTH)]

    display = None
    initialColor = None

    changes = None

    def __init__(self, display, initialColor):
        """
        :param PCD8544DisplayComponent display
        :param initialColor color
        """
        self.display = display
        self.initialColor = initialColor

        self.changes = deque()

        for x in range(DisplayDataRamSize.DDRAM_WIDTH):
            for y in range(DisplayDataRamSize.DDRAM_HEIGHT):
                bank = PCB8544DDRamBank(x, y, initialColor)
                self.dataBuffer[x][y] = bank
                self.changes.append(bank)

    def setPixel(self, x, y, color):
        if not self._isPositionExists(x, y):
            raise IndexError("Position ("+x+", "+y+") don't exists")

        if not (color == MonochomaticDisplay.DARK) and \
           not (color == MonochomaticDisplay.LIGHT):
            raise Exception("The color should be MonochomaticDisplay.DARK or MonochomaticDisplay.LIGHT!")

        bank = self.getBank(x, y)
        anotherChangeRegistred = bank.hasChanged()

        bank.setPixel(y % 8, color)

        if bank.hasChanged() and not anotherChangeRegistred:
            self.changes.append(bank)

    def getBank(self, x, y):
        """
        :param int x:
        :param int y:
        :return PCD8544DDRamBank:
        """
        return self.dataBuffer[x][int(y/8)]

    def getPixel(self, x, y):
        """
        :param int x:
        :param int y:
        """
        if not self._isPositionExists(x, y):
            raise IndexError("Position (" + str(x) + ", " + str(y) + ") don't exists")

        return self.getBank(x, y).getPixel(y)

    def _isPositionExists(self, x, y):
        notExists = x < 0 \
                 or y < 0 \
                 or x >= self.display.width \
                 or y >= self.display.height
        return not notExists

    def clear(self):
        for x in range(DisplaySize.WIDTH):
            for y in range(DisplaySize.HEIGHT):
                self.setPixel(x, y, self.initialColor)