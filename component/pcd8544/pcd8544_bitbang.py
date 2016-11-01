# -*- coding: utf-8 -*-
import ctypes
import time

from display_graphics import DisplayGraphics
from pcd8544_constants import DisplaySize, SysCommand, Setting

import numpy
from gpiozero import DigitalOutputDevice


class PCD8544(object):
    """
    PCD8544 display implementation.

    This implementation uses software shiftOut implementation?

    @author SrMouraSilva
    Based in 2013 Giacomo Trudu - wicker25[at]gmail[dot]com
    Based in 2010 Limor Fried, Adafruit Industries
          https://github.com/adafruit/Adafruit_Nokia_LCD/blob/master/Adafruit_Nokia_LCD/PCD8544.py
    Based in CORTEX-M3 version by Le Dang Dung, 2011 LeeDangDung@gmail.com (tested on LPC1769)
    Based in Raspberry Pi version by Andre Wussow, 2012, desk@binerry.de
    Based in Raspberry Pi Java version by Cleverson dos Santos Assis, 2013, tecinfcsa@yahoo.com.br


    https://www.raspberrypi.org/documentation/hardware/raspberrypi/spi/README.md

    The SPI master driver is disabled by default on Raspbian.
    To enable it, use raspi-config, or ensure the line
    dtparam=spi=on isn't commented out in /boot/config.txt, and reboot.

    :param int din: Serial data input
    :param int sclk: Serial clock input (clk)
    :param int dc: Data/Command mode select (d/c)
    :param int rst: External reset input (res)
    :param int cs: Chip Enable (CS/SS, sce)

    :param contrast
    :param inverse
    """
    def __init__(self, din, sclk, dc, rst, cs, contrast=60, inverse=False):
        self.DC = DigitalOutputDevice(dc)
        self.RST = DigitalOutputDevice(rst)

        self.clock_pin = ctypes.c_uint8(sclk)
        self.data_pin = ctypes.c_uint8(din)
        self.not_enable = DigitalOutputDevice(cs)

        #lib = './wiring_bitbang.so'
        lib = './native_bitbang.so'
        self.bitbang = ctypes.cdll.LoadLibrary(lib)
        self.bitbang.init(self.data_pin, self.clock_pin)

        self._reset()
        self._init(contrast, inverse)

        self.drawer = DisplayGraphics(self)
        self.clear()
        self.dispose()

    def _reset(self):
        self.RST.off()
        time.sleep(0.100)
        self.RST.on()

    def _init(self, contrast, inverse):
        # H = 1
        self._send_command(SysCommand.FUNC | Setting.FUNC_H)
        self._send_command(SysCommand.BIAS | Setting.BIAS_BS2)
        self._send_command(SysCommand.VOP | contrast & 0x7f)
        # H = 0
        self._send_command(SysCommand.FUNC | Setting.FUNC_V)
        self._send_command(
            SysCommand.DISPLAY |
            Setting.DISPLAY_D |
            Setting.DISPLAY_E * (1 if inverse else 0)
        )

    def _send_command(self, data):
        self.DC.off()

        self._write([data])

    def _send_data_byte(self, x, y, byte):

        self._set_cursor_x(x)
        self._set_cursor_y(y)

        self.DC.on()

        self._write([byte])

    def set_contrast(self, value):
        self._send_command(SysCommand.FUNC | Setting.FUNC_H)
        self._send_command(SysCommand.VOP | value & 0x7f)
        self._send_command(SysCommand.FUNC | Setting.FUNC_V)

    def write_all(self, data):
        """
        :param list[int] data:
        """
        self._set_cursor_x(0)
        self._set_cursor_y(0)

        self.DC.on()

        self._write(data)

    def _write(self, data):
        self.not_enable.off()

        array = numpy.array(data).astype(numpy.uint8).ctypes.data
        size = ctypes.c_uint32(len(data))
        data_pointer = ctypes.c_void_p(array)

        self.bitbang.bitbang_shift_out(data_pointer, size, self.data_pin, self.clock_pin)

        self.not_enable.on()

    def _set_cursor_x(self, x):
        self._send_command(SysCommand.XADDR | x)

    def _set_cursor_y(self, y):
        self._send_command(SysCommand.YADDR | y)

    def clear(self):
        self._set_cursor_x(0)
        self._set_cursor_y(0)

        self.drawer.clear()

    @property
    def width(self):
        return DisplaySize.WIDTH

    @property
    def height(self):
        return DisplaySize.HEIGHT

    @property
    def value(self):
        return 0

    def close(self):
        pass

    @property
    def draw(self):
        return self.drawer.draw

    def dispose(self):
        self.drawer.dispose()
