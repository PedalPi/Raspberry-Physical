# -*- coding: utf-8 -*-
from collections import deque

from monochomatic_display import MonochomaticDisplay
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

    data_buffer = [[None] * DisplayDataRamSize.DDRAM_HEIGHT for _ in range(DisplayDataRamSize.DDRAM_WIDTH)]

    display = None
    initial_color = None

    changes = None

    def __init__(self, display, initial_color):
        """
        :param PCD8544DisplayComponent display:
        :param Color initial_color:
        """
        self.display = display
        self.initial_color = initial_color

        self.changes = deque()

        for x in range(DisplayDataRamSize.DDRAM_WIDTH):
            for y in range(DisplayDataRamSize.DDRAM_HEIGHT):
                bank = PCB8544DDRamBank(x, y, initial_color)
                self.data_buffer[x][y] = bank
                self.changes.append(bank)

    def set_pixel(self, x, y, color):
        if not self._is_position_exists(x, y):
            raise IndexError("Position ("+x+", "+y+") don't exists")

        if not (color == MonochomaticDisplay.DARK) and \
           not (color == MonochomaticDisplay.LIGHT):
            raise Exception("The color should be MonochromaticDisplay.DARK or Monochromatic.LIGHT!")

        bank = self.get_bank(x, y)
        another_change_registered = bank.changed

        bank.setPixel(y % 8, color)

        if bank.changed and not another_change_registered:
            self.changes.append(bank)

    def get_bank(self, x, y):
        """
        :param int x:
        :param int y:
        :return PCD8544DDRamBank:
        """
        return self.data_buffer[x][int(y / 8)]

    def getPixel(self, x, y):
        """
        :param int x:
        :param int y:
        """
        if not self._is_position_exists(x, y):
            raise IndexError("Position (" + str(x) + ", " + str(y) + ") don't exists")

        return self.get_bank(x, y).getPixel(y)

    def _is_position_exists(self, x, y):
        not_exists = x < 0 \
                  or y < 0 \
                  or x >= self.display.width \
                  or y >= self.display.height
        return not not_exists

    def clear(self):
        for x in range(DisplaySize.WIDTH):
            for y in range(DisplaySize.HEIGHT):
                self.set_pixel(x, y, self.initial_color)
