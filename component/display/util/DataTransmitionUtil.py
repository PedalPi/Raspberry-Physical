# -*- coding: utf-8 -*-

from enum import Enum


class BitOrderFirst(Enum):
    LSB = 1
    MSB = 2


class DataTransmitionUtil:
    """
    Utils for change data transmittion

    @author SrMouraSilva
    Based in 2013 Giacomo Trudu - wicker25[at]gmail[dot]com
    Based in 2010 Limor Fried, Adafruit Industries
    Based in CORTEX-M3 version by Le Dang Dung, 2011 LeeDangDung@gmail.com (tested on LPC1769)
    Based in Raspberry Pi version by Andre Wussow, 2012, desk@binerry.de
    Based in Raspberry Pi Java version by Cleverson dos Santos Assis, 2013, tecinfcsa@yahoo.com.br
    """

    @staticmethod
    def shiftOut(data, dataPin, clockPin, order):
        """
        :deprecated FIXME Use native shiftOut!

        :param byte data
        :param GpioPinDigitalOutput dataPin
        :param GpioPinDigitalOutput clockPin
        :param BitOrderFirst order
        """
        if order == BitOrderFirst.MSB:
            DataTransmitionUtil.writeDataMSBFirst(data, dataPin, clockPin)
        else:
            DataTransmitionUtil.writeDataLSBFirst(data, dataPin, clockPin)

    @staticmethod
    def writeDataLSBFirst(data, dataPin, clockPin):
        """
        :param byte data
        :param GpioPinDigitalOutput dataPin
        :param GpioPinDigitalOutput clockPin
        """
        DataTransmitionUtil.write(data, dataPin, clockPin, range(8))

    @staticmethod
    def writeDataMSBFirst(data, dataPin, clockPin):
        """
        :param byte data
        :param GpioPinDigitalOutput dataPin
        :param GpioPinDigitalOutput clockPin
        """
        DataTransmitionUtil.write(data, dataPin, clockPin, reversed(range(8)))

    @staticmethod
    def write(data, dataPin, clockPin, rangeOrder):
        """
        :param byte data
        :param GpioPinDigitalOutput dataPin
        :param GpioPinDigitalOutput clockPin
        :param list rangeOrder: bits order to send
        """
        for i in rangeOrder:
            bitState = DataTransmitionUtil.bitState(data, i)
            dataPin.on() if bitState else dataPin.off()

            DataTransmitionUtil.toggleClock(clockPin)

    @staticmethod
    def bitState(data, i):
        return (data & (1 << i)) >> i == 1

    @staticmethod
    def toggleClock(clock):
        """
        :param GpioPinDigitalOutput clock
        """
        clock.on()
        # The pin changes usign wiring pi are 20ns?
        # The pi4j in Snapshot 1.1.0 are 1MHz ~ 1 microssecond in Raspberry 2      http://www.savagehomeautomation.com/projects/raspberry-pi-with-java-programming-the-internet-of-things-io.html#follow_up_pi4j
        # Its necessary only 10ns    Pag 22 - https://www.sparkfun.com/datasheets/LCD/Monochrome/Nokia5110.pdf
        # Not discoment :D
        #Gpio.delayMicroseconds(CLOCK_TIME_DELAY);
        clock.off()
