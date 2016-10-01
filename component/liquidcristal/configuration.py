from util import usleep, msleep


class Configuration8Pins(object):
    def __init__(self, lcd):
        self.LCD = lcd

    def initialize_display(self):
        msleep(50)

        self.LCD.rs.off()
        if self.LCD.rw is not None:
            self.LCD.rw.off()

        self._write_4bits(0x03)
        msleep(4.5)
        self._write_4bits(0x03)
        usleep(100)
        self._write_4bits(0x03)

        usleep(100)

    def write_byte(self, byte):
        self.LCD.enable.off()

        self._write_pins(byte)

        usleep(2)
        self.LCD.enable.on()
        usleep(5)
        self.LCD.enable.off()

    def _write_pins(self, data):
        self.LCD.db7.value = (data & 0b10000000) >> 7 == 1
        self.LCD.db6.value = (data & 0b01000000) >> 6 == 1
        self.LCD.db5.value = (data & 0b00100000) >> 5 == 1
        self.LCD.db4.value = (data & 0b00010000) >> 4 == 1
        self.LCD.db3.value = (data & 0b00001000) >> 3 == 1
        self.LCD.db2.value = (data & 0b00000100) >> 2 == 1
        self.LCD.db1.value = (data & 0b00000010) >> 1 == 1
        self.LCD.db0.value = (data & 0b00000001) == 1


class Configuration4Pins(object):
    def __init__(self, lcd):
        self.LCD = lcd

    def initialize_display(self):
        msleep(50)

        self.LCD.rs.off()
        if self.LCD.rw is not None:
            self.LCD.rw.off()

        self._write_4bits(0x03)
        msleep(4.5)
        self._write_4bits(0x03)
        usleep(100)
        self._write_4bits(0x03)

        self._write_4bits(0x02)
        usleep(100)

    def write_byte(self, byte):
        self._write_4bits(byte >> 4)
        self._write_4bits(byte)

    def _write_4bits(self, data):
        self.LCD.enable.off()

        self._write_pins(data)

        usleep(2)
        self.LCD.enable.on()
        usleep(5)
        self.LCD.enable.off()

    def _write_pins(self, data):
        self.LCD.db7.value = (data & 0b00001000) >> 3 == 1
        self.LCD.db6.value = (data & 0b00000100) >> 2 == 1
        self.LCD.db5.value = (data & 0b00000010) >> 1 == 1
        self.LCD.db4.value = (data & 0b00000001) == 1
