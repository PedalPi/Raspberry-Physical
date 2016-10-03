# -*- coding: utf-8 -*-
import time

from gpiozero import DigitalOutputDevice, PWMOutputDevice
from gpiozero import SPIDevice

from util.Color import Color

from MonochomaticDisplay import MonochomaticDisplay
from impl.pcd8544.PCB8544DisplayDataRam import PCB8544DisplayDataRam
from impl.pcd8544.PCD8544Constants import DisplaySize, SysCommand, Setting

from util.DataTransmitionUtil import BitOrderFirst, DataTransmitionUtil


class PCD8544(MonochomaticDisplay):
#class PCD8544(SPIDevice):
    '''
    PCD8544 display implementation.

    This implementation uses software shiftOut implementation?

    @author SrMouraSilva
    Based in 2013 Giacomo Trudu - wicker25[at]gmail[dot]com
    Based in 2010 Limor Fried, Adafruit Industries
          https://github.com/adafruit/Adafruit_Nokia_LCD/blob/master/Adafruit_Nokia_LCD/PCD8544.py
    Based in CORTEX-M3 version by Le Dang Dung, 2011 LeeDangDung@gmail.com (tested on LPC1769)
    Based in Raspberry Pi version by Andre Wussow, 2012, desk@binerry.de
    Based in Raspberry Pi Java version by Cleverson dos Santos Assis, 2013, tecinfcsa@yahoo.com.br
    '''
    DDRAM = None

    """ Data/Command mode select """
    DC = None
    """ External reset input """
    RST = None

    def __init__(self, din, sclk, dc, rst, cs, contrast=60, inverse=False):
        """
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
        #super(PCD8544, self).__init__(clock_pin=sclk, mosi_pin=din, miso_pin=1, select_pin=cs)
        self.DDRAM = PCB8544DisplayDataRam(self, Color.WHITE)

        self.DIN = DigitalOutputDevice(din)
        self.SCLK = DigitalOutputDevice(sclk)
        self.DC = DigitalOutputDevice(dc)
        self.RST = DigitalOutputDevice(rst)
        self.SCE = DigitalOutputDevice(cs)

        self._reset()
        self._init(contrast, inverse)

        self.redraw()

    def _reset(self):
        self.RST.off()
        time.sleep(0.100)
        self.RST.on()

    def _init(self, contrast, inverse):
        # H = 1
        self._sendCommand(SysCommand.FUNC | Setting.FUNC_H)
        self._sendCommand(SysCommand.BIAS | Setting.BIAS_BS2)
        self._sendCommand(SysCommand.VOP | contrast & 0x7f)
        # H = 0
        self._sendCommand(SysCommand.FUNC)
        self._sendCommand(
            SysCommand.DISPLAY |
            Setting.DISPLAY_D |
            Setting.DISPLAY_E * (1 if inverse else 0)
        )

    def _sendCommand(self, data):
        self.SCE.off()
        self.DC.off()

        #self._spi.write([data])
        self._writeDataShiftOut(data)

        self.SCE.on()

    def _writeDataShiftOut(self, data):
        DataTransmitionUtil.shiftOut(
            data,
            self.DIN,
            self.SCLK,
            BitOrderFirst.MSB
        )

    def _toggleClock(self):
        self.SCLK.on()
        # The pin changes usign wiring pi are 20ns?
        # The pi4j in Snapshot 1.1.0 are 1MHz ~ 1 microssecond in Raspberry 2
        #  http://www.savagehomeautomation.com/projects/raspberry-pi-with-java-programming-the-internet-of-things-io.html#follow_up_pi4j
        # Its necessary only 10ns
        #  Pag 22 - https://www.sparkfun.com/datasheets/LCD/Monochrome/Nokia5110.pdf
        # Not discoment :D
        #Gpio.delayMicroseconds(CLOCK_TIME_DELAY);
        self.SCLK.off()

    def setContrast(self, value):
        self._sendCommand(SysCommand.FUNC | Setting.FUNC_H)
        self._sendCommand(SysCommand.VOP | value & 0x7f)
        self._sendCommand(SysCommand.FUNC)

    def setPixel(self, x, y, color):
        self.DDRAM.setPixel(x, y, color)

    def getPixel(self, x, y):
        return self.DDRAM.getPixel(x, y)

    def redraw(self):
        print("Realizando redraw")
        changes = self.DDRAM.changes
        print("Total de mudanças: ", len(changes))

        import time
        start_time = time.time()

        while changes:
            bank = changes.popleft()
            self._sendDataByte(bank.x, bank.y, bank.mbs_byte)
            bank.setChanged(False)

        print("--- %s seconds ---" % (time.time() - start_time))

    def _sendDataByte(self, x, y, byte):
        self._setCursorX(x)
        self._setCursorY(y)

        self.SCE.off()
        self.DC.on()
        self._writeDataShiftOut(byte)
        #self._spi.write([byte])
        self.SCE.on()

    def redraw_test(self, pixelss):
        print("Realizando redraw_test")
        self._setCursorX(0)
        self._setCursorY(0)

        import time
        start_time = time.time()

        self.SCE.off()
        self.DC.on()
        for pixels in pixelss:
            for pixel in pixels:
                if pixel == Color.BLACK:
                    self.DIN.on()
                else:
                    self.DIN.off()
                self._toggleClock()

        self.SCE.on()
        print("--- %s seconds ---" % (time.time() - start_time))

    def _sendDataByte(self, x, y, byte):
        self._setCursorX(x)
        self._setCursorY(y)

        self.SCE.off()
        self.DC.on()
        self._writeDataShiftOut(byte)
        # self._spi.write([byte])
        self.SCE.on()

    def _setCursorX(self, x):
        self._sendCommand(SysCommand.XADDR | x)

    def _setCursorY(self, y):
        self._sendCommand(SysCommand.YADDR | y)

    def clear(self):
        self.DDRAM.clear()

        self._setCursorX(0)
        self._setCursorY(0)

    @property
    def width(self):
        return DisplaySize.WIDTH

    @property
    def height(self):
        return DisplaySize.HEIGHT
