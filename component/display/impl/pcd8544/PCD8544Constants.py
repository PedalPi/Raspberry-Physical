# -*- coding: utf-8 -*-
'''
Group the PCD8544 constants

@author SrMouraSilva
Based in <a href="https://github.com/Wicker25/Rpi-hw/blob/db4d9c0dd9d765a3f92f63b6aa413316f01be15e/include/rpi-hw/display/pcd8544.hpp">Rpi-hd PCD8544 implementation</a>
'''

class SysCommand(object):
    '''Display control'''
    DISPLAY = 0x08
    '''Function set'''
    FUNC    = 0x20
    '''Set Y address of RAM'''
    YADDR   = 0x40
    '''Set Y address of RAM'''
    XADDR   = 0x80

    '''Temperature control'''
    TEMP    = 0x04
    '''Bias system'''
    BIAS    = 0x10
    '''Set Vop'''
    VOP     = 0x80

class Setting(object):
    '''Sets display configuration'''
    DISPLAY_E    = 0x01
    '''Sets display configuration'''
    DISPLAY_D    = 0x04

    '''Extended instruction set'''
    FUNC_H       = 0x01
    '''Entry mode'''
    FUNC_V       = 0x02
    '''Power down control'''
    FUNC_PD      = 0x04

    '''Set bias system'''
    BIAS_BS0     = 0x01
    '''Set bias system'''
    BIAS_BS1    = 0x02
    '''Set bias system'''
    BIAS_BS2    = 0x04

class DisplaySize(object):
    WIDTH  = 84
    HEIGHT = 48
