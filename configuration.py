# -*- coding: utf-8 -*-
from components import PatchButton


class Configuration(object):

    def __init__(self):
        self.display = None
        self.nextPatchButton = PatchButton(21)
        self.beforePatchButton = PatchButton(20)
        self.effectButtons = []
