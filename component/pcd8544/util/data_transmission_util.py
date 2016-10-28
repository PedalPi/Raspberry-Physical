# -*- coding: utf-8 -*-

from enum import Enum


class BitOrderFirst(Enum):
    LSB = 1
    MSB = 2


class DataTransmissionUtil:
    """
    Utils for change data transmission

    @author SrMouraSilva
    Based in 2013 Giacomo Trudu - wicker25[at]gmail[dot]com
    Based in 2010 Limor Fried, Adafruit Industries
    Based in CORTEX-M3 version by Le Dang Dung, 2011 LeeDangDung@gmail.com (tested on LPC1769)
    Based in Raspberry Pi version by Andre Wussow, 2012, desk@binerry.de
    Based in Raspberry Pi Java version by Cleverson dos Santos Assis, 2013, tecinfcsa@yahoo.com.br
    """

    @staticmethod
    def shift_out(data, data_pin, clock_pin, order):
        """
        :deprecated FIXME Use native shiftOut!
        """
        if order == BitOrderFirst.MSB:
            DataTransmissionUtil.write_data_mbs_first(data, data_pin, clock_pin)
        else:
            DataTransmissionUtil.write_data_lsb_first(data, data_pin, clock_pin)

    @staticmethod
    def write_data_mbs_first(data, data_pin, clock_pin):
        DataTransmissionUtil.write(data, data_pin, clock_pin, range(8))

    @staticmethod
    def write_data_lsb_first(data, data_pin, clock_pin):
        DataTransmissionUtil.write(data, data_pin, clock_pin, reversed(range(8)))

    @staticmethod
    def write(data, data_pin, clock_pin, range_order):
        """
        :param byte data:
        :param DigitalOutput data_pin:
        :param DigitalOutput clock_pin:
        :param list range_order: bits order to send
        """
        for i in range_order:
            bit_state = DataTransmissionUtil.bit_state(data, i)
            data_pin.on() if bit_state else data_pin.off()

            DataTransmissionUtil.toggle_clock(clock_pin)

    @staticmethod
    def bit_state(data, i):
        return (data & (1 << i)) >> i == 1

    @staticmethod
    def toggle_clock(clock):
        clock.on()
        # The pin changes usign wiring pi are 20ns?
        # The pi4j in Snapshot 1.1.0 are 1MHz ~ 1 microssecond in Raspberry 2
        #  http://www.savagehomeautomation.com/projects/raspberry-pi-with-java-programming-the-internet-of-things-io.html#follow_up_pi4j
        # Its necessary only 10ns    Pag 22 - https://www.sparkfun.com/datasheets/LCD/Monochrome/Nokia5110.pdf
        # Not discoment :D
        #Gpio.delayMicroseconds(CLOCK_TIME_DELAY);
        #time.sleep(0.000002)
        clock.off()
