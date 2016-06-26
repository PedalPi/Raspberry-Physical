# -*- coding: utf-8 -*-
from time import sleep

from gpiozero import DigitalOutputDevice

from util.privatemethod import privatemethod
from util.Color import Color
from util.DataTransmitionUtil import BitOrderFirst, DataTransmitionUtil

from MonochomaticDisplay import MonochomaticDisplay
from impl.pcd8544.PCB8544DisplayDataRam import PCB8544DisplayDataRam
from impl.pcd8544.PCD8544Constants import DisplaySize, SysCommand, Setting


class PCD8544DisplayComponent(MonochomaticDisplay):
    '''
    PCD8544 display implementation.

    This implementation uses software shiftOut implementation

    @author SrMouraSilva
    Based in 2013 Giacomo Trudu - wicker25[at]gmail[dot]com
    Based in 2010 Limor Fried, Adafruit Industries
          https://github.com/adafruit/Adafruit_Nokia_LCD/blob/master/Adafruit_Nokia_LCD/PCD8544.py
    Based in CORTEX-M3 version by Le Dang Dung, 2011 LeeDangDung@gmail.com (tested on LPC1769)
    Based in Raspberry Pi version by Andre Wussow, 2012, desk@binerry.de
    Based in Raspberry Pi Java version by Cleverson dos Santos Assis, 2013, tecinfcsa@yahoo.com.br
    '''

    #private static final int CLOCK_TIME_DELAY = 1;//micro seconds // 10 nanosseconds is the correct
    #http://stackoverflow.com/questions/11498585/how-to-suspend-a-java-thread-for-a-small-period-of-time-like-100-nanoseconds
    RESET_DELAY = 1 #10^-3ms is the correct

    DDRAM = None

    ''' Serial data input '''
    DIN = None
    ''' Input for the clock signal '''
    SCLK = None
    ''' Data/Command mode select '''
    DC = None
    ''' External rst input '''
    RST = None
    ''' Chip Enable (CS/SS) '''
    SCE = None

    def __init__(self, din, sclk, dc, rst, cs, contrast=60, inverse=False):
        """
        :param int din: Serial data input.
        :param int sclk: Input for the clock signal.
        :param int dc: Data/Command mode select.
        :param int rst: External rst input.
        :param int cs: Chip Enable (CS/SS)

        :param contrast
        :param inverse
        """
        self.DDRAM = PCB8544DisplayDataRam(self, Color.WHITE)

        self.DIN = DigitalOutputDevice(din)
        self.SCLK = DigitalOutputDevice(sclk)
        self.DC = DigitalOutputDevice(dc)
        self.RST = DigitalOutputDevice(rst)
        self.SCE = DigitalOutputDevice(cs)

        self.reset()
        self.init(contrast, inverse)

        self.redraw()
        print("redrou")
        print("Pronto")

    @privatemethod
    def reset(self):
        self.RST.off()
        #sleep(1)
        self.RST.on()

    @privatemethod
    def init(self, contrast, inverse):
        self.sendCommand(SysCommand.FUNC | Setting.FUNC_H)
        self.sendCommand(SysCommand.BIAS | 0x04)
        self.sendCommand(SysCommand.VOP | contrast & 0x7f)
        self.sendCommand(SysCommand.FUNC)
        self.sendCommand(
            SysCommand.DISPLAY |
            Setting.DISPLAY_D |
            Setting.DISPLAY_E * (1 if inverse else 0)
        )

    @privatemethod
    def sendCommand(self, data):
        self.DC.off()

        self.SCE.off()
        self.writeDataCommand(data)
        self.SCE.on()

    @privatemethod
    def writeDataCommand(self, data):
        DataTransmitionUtil.shiftOut(
            data,
            self.DIN,
            self.SCLK,
            BitOrderFirst.MSB
        )

    @privatemethod
    def toggleClock(self):
        self.SCLK.on()
        # The pin changes usign wiring pi are 20ns?
        # The pi4j in Snapshot 1.1.0 are 1MHz ~ 1 microssecond in Raspberry 2
        #  http://www.savagehomeautomation.com/projects/raspberry-pi-with-java-programming-the-internet-of-things-io.html#follow_up_pi4j
        # Its necessary only 10ns
        #  Pag 22 - https://www.sparkfun.com/datasheets/LCD/Monochrome/Nokia5110.pdf
        # Not discoment :D
        #Gpio.delayMicroseconds(CLOCK_TIME_DELAY);
        self.SCLK.off()

    @privatemethod
    def setContrast(self, value):
        self.sendCommand(SysCommand.FUNC, Setting.FUNC_H)
        self.sendCommand(SysCommand.VOP, value & 0x7f)
        self.sendCommand(SysCommand.FUNC)

    def setPixel(self, x, y, color):
        self.DDRAM.setPixel(x, y, color)

    def getPixel(self, x, y):
        return self.DDRAM.getPixel(x, y)

    def redraw(self):
        changes = self.DDRAM.changes
        while len(changes) != 0:
            print(len(changes))
            bank = changes.popleft()
            self.setCursorY(bank.y)
            self.setCursorX(bank.x)

            self.sendData(bank)

    @privatemethod
    def sendData(self, bank):
        """
        :param PCB8544DDRamBank bank
        """
        self.DC.on()

        self.SCE.off()
        self.writeData(bank)
        self.SCE.on()

    @privatemethod
    def writeData(self, bank):
        iterator = bank.msbIterator()
        while iterator.hasNext():
            color = iterator.nextElement()
            if color == Color.BLACK:
                self.DIN.on()
            else:
                self.DIN.off()

            self.toggleClock()

        bank.setChanged(False)

    @privatemethod
    def setCursorX(self, x):
        self.sendCommand(SysCommand.XADDR | x)

    @privatemethod
    def setCursorY(self, y):
        self.sendCommand(SysCommand.YADDR | y)

    def clear(self):
        self.DDRAM.clear()

        self.setCursorX(0)
        self.setCursorY(0)

    @property
    def width(self):
        return DisplaySize.WIDTH

    @property
    def height(self):
        return DisplaySize.HEIGHT
