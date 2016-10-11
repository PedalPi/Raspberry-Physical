# -*- coding: utf-8 -*-
from abc import ABCMeta
from display import Display
from util.color import Color


class MonochomaticDisplay(Display, metaclass=ABCMeta):
    """
    A simple Interface to mark the Monochomatic Displays
    """

    DARK = Color.BLACK
    LIGHT = Color.WHITE
