# -*- coding: utf-8 -*-
import time

from gpiozero import DigitalOutputDevice, PWMOutputDevice
from gpiozero import SPIDevice

from util.color import Color

from impl.pcd8544.PCB8544DisplayDataRam import PCB8544DisplayDataRam
from impl.pcd8544.PCD8544Constants import DisplaySize, SysCommand, Setting


class PCD8544(SPIDevice):
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
        super(PCD8544, self).__init__(clock_pin=sclk, mosi_pin=din, miso_pin=9, select_pin=cs)
        self.DDRAM = PCB8544DisplayDataRam(self, Color.WHITE)

        self.DC = DigitalOutputDevice(dc)
        self.RST = DigitalOutputDevice(rst)

        self._reset()
        self._init(contrast, inverse)

        self.redraw()

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

        self._spi.write([data])

    def _send_data_byte(self, x, y, byte):
        self._set_cursor_x(x)
        self._set_cursor_y(y)

        self.DC.on()
        self._spi.write([byte])

    def set_contrast(self, value):
        self._send_command(SysCommand.FUNC | Setting.FUNC_H)
        self._send_command(SysCommand.VOP | value & 0x7f)
        self._send_command(SysCommand.FUNC | Setting.FUNC_V)

    def set_pixel(self, x, y, color):
        self.DDRAM.set_pixel(x, y, color)

    def get_pixel(self, x, y):
        return self.DDRAM.getPixel(x, y)

    def write_all(self, data):
        self._set_cursor_x(0)
        self._set_cursor_y(0)

        self.DC.on()
        self._spi.write(data)

    def redraw(self):
        changes = self.DDRAM.changes

        while changes:
            bank = changes.popleft()
            self._send_data_byte(bank.x, bank.y, bank.mbs_byte)
            bank.changed = False

    def _set_cursor_x(self, x):
        self._send_command(SysCommand.XADDR | x)

    def _set_cursor_y(self, y):
        self._send_command(SysCommand.YADDR | y)

    def clear(self):
        self.DDRAM.clear()

        self._set_cursor_x(0)
        self._set_cursor_y(0)

    @property
    def width(self):
        return DisplaySize.WIDTH

    @property
    def height(self):
        return DisplaySize.HEIGHT
