# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod


class Display(metaclass=ABCMeta):

    @abstractmethod
    def setPixel(self, x, y, color):
        """
        Set a specific pixel for a color

        :param x Row position. 0 is first, top to down direction
        :param y Column position. 0 is first, left to right direction
        :param color
        """
        ...

    @abstractmethod
    def redraw(self):
        """
        Repaint the display, updating changes caused by use of setPixel method
        """
        ...

    @abstractmethod
    def clear(self):
        """
        Change the Display for initial stage
        """
        ...

    @property
    @abstractmethod
    def width(self):
        ...

    @property
    @abstractmethod
    def height(self):
        ...

