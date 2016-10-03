from util import usleep, msleep


class AbstractConfigurationPins(object):
    def __init__(self, lcd):
        self.LCD = lcd

    def initialize_display(self):
        msleep(50)

        self.LCD.rs.off()
        if self.LCD.rw is not None:
            self.LCD.rw.off()

        self.initialize()

        usleep(100)

    def initialize(self):
        raise NotImplementedError()

    def write_4_bits(self, data):
        self._write(ParallelBitsWriter.write_4_pins, data)

    def write_8_bits(self, data):
        self._write(ParallelBitsWriter.write_8_pins, data)

    def _write(self, method, data):
        self.LCD.enable.off()
        method(self.LCD, data)
        self._clock_enable()

    def _clock_enable(self):
        usleep(2)
        self.LCD.enable.on()
        usleep(5)
        self.LCD.enable.off()


class Configuration8Pins(AbstractConfigurationPins):
    def __init__(self, lcd):
        super().__init__(lcd)

    def initialize(self):
        self.write_4_bits(0x03)
        msleep(4.5)
        self.write_4_bits(0x03)
        usleep(100)
        self.write_4_bits(0x03)

    def write_byte(self, byte):
        self.write_8_bits(byte)


class Configuration4Pins(AbstractConfigurationPins):
    def __init__(self, lcd):
        super().__init__(lcd)

    def initialize(self):
        self.write_4_bits(0x03)
        msleep(4.5)
        self.write_4_bits(0x03)
        usleep(100)
        self.write_4_bits(0x03)

        self.write_4_bits(0x02)

    def write_byte(self, byte):
        self.write_4_bits(byte >> 4)
        self.write_4_bits(byte)


class ParallelBitsWriter(object):

    @staticmethod
    def write_4_pins(lcd, data):
        lcd.db7.value = (data & 0b00001000) >> 3 == 1
        lcd.db6.value = (data & 0b00000100) >> 2 == 1
        lcd.db5.value = (data & 0b00000010) >> 1 == 1
        lcd.db4.value = (data & 0b00000001) == 1

    @staticmethod
    def write_8_pins(lcd, data):
        lcd.db7.value = (data & 0b10000000) >> 7 == 1
        lcd.db6.value = (data & 0b01000000) >> 6 == 1
        lcd.db5.value = (data & 0b00100000) >> 5 == 1
        lcd.db4.value = (data & 0b00010000) >> 4 == 1
        lcd.db3.value = (data & 0b00001000) >> 3 == 1
        lcd.db2.value = (data & 0b00000100) >> 2 == 1
        lcd.db1.value = (data & 0b00000010) >> 1 == 1
        lcd.db0.value = (data & 0b00000001) == 1
