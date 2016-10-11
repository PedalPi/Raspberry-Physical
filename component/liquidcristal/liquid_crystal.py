import time
from gpiozero import DigitalOutputDevice, SharedMixin, Device
from command import Command
from util import msleep, usleep, ByteUtil
from configuration import Configuration4Pins


def lcd(rs, enable, rw=None, **kwargs):
    lcd = LiquidCrystal(**kwargs)
    lcd._init(rs, enable, rw, **kwargs)

    return lcd

class LiquidCrystal(SharedMixin, Device):
    """
    Based in https://www.sparkfun.com/datasheets/LCD/HD44780.pdf
    """
    rows = 2
    columns = 16

    row = 0
    column = 0

    content = None

    db7 = None
    db6 = None
    db5 = None
    db4 = None

    enable = None
    rs = None
    rw = None

    _entry_mode = Command.ENTRY_MODE_SET | Command.MODE_INCREMENT | Command.NOT_ACCOPANIES_DISPLAY_SHIFT
    _display_control = Command.DISPLAY_ON_OFF_CONTROL | Command.DISPLAY_ON | Command.CURSOR_ON | Command.BLINKING_ON

    def __init__(self, db7, db6, db5, db4):
        super(Device, self).__init__()

        self.content = [[0x20] * self.columns for _ in range(self.rows)]

        self.strategy = Configuration4Pins(self)

    def _init(self, rs, enable, rw=None, **kwargs):
        self._init_pins(rs, enable, rw, **kwargs)
        self._init_display()

    #@staticmethod
    #def _shared_key(cls, db7, db6, db5, db4):
    #    return (db7, db6, db5, db4)

    def _init_pins(self, rs, enable, rw, db7, db6, db5, db4):
        self.db7 = DigitalOutputDevice(db7)
        self.db6 = DigitalOutputDevice(db6)
        self.db5 = DigitalOutputDevice(db5)
        self.db4 = DigitalOutputDevice(db4)
        #self.db3 = DigitalOutputDevice()
        #self.db2 = DigitalOutputDevice()
        #self.db1 = DigitalOutputDevice()
        #self.db0 = DigitalOutputDevice()

        self.rs = DigitalOutputDevice(rs)
        if rw is None:
            self.rw = None
        else:
            self.rw = DigitalOutputDevice(rw)
        self.enable = DigitalOutputDevice(enable)

    def _init_display(self):
        self.strategy.initialize_display()

        self.command(Command.FUNCTION_SET | Command.TWO_ROWS | Command.CHARACTER_5x7)
        self.command(Command.CURSOR_OR_DISPLAY_MOVE | Command.CURSOR_MOVE | Command.MOVE_LEFT)
        self.clear()
        self.command(self._display_control)

    def command(self, command):
        """
        Send a command to display
        Please, use Command static attributes to splicit code
        """
        self._write_data(True, command)

    def data(self, char):
        """
        Send data to display
        If you request send text, please, use self.write() method
        """
        self._write_data(False, char)

    def _write_data(self, is_command, byte):
        self.rs.value = not is_command

        self.strategy.write_byte(byte)

        usleep(50)  # HD44780: > 37us

    def _write_byte(self, data):
        self.strategy.write_byte(data)

    def write(self, string, row=None, column=None):
        if row is None:
            row = self.position[0]
        if column is None:
            column = self.position[1]

        self.position = (row, column)

        for char in string:
            byte_char = ord(char)
            self.data(byte_char)
            self.content[self.row][self.column] = byte_char

    @property
    def position(self):
        return self.row, self.column

    @position.setter
    def position(self, position):
        self.row, self.column = position[0], position[1]

        data = Command.ROWS[self.row] | self.column
        self.command(data)

    def clear(self):
        self.row = 0
        self.column = 0

        self.content = [[None] * self.columns for _ in range(self.rows)]

        self.command(Command.CLEAR)
        msleep(2)  # Clear requests more time than another Command

    def home(self):
        """Return to initial position (row=0, column=0)"""
        self.row = 0
        self.column = 0

        self.command(Command.RETURN_HOME)
        msleep(2)  # Got to home requests more time than another Command

    @property
    def visible(self):
        """return bool: Is display visible?"""
        return ByteUtil.is_flag_active(self._display_control, Command.DISPLAY_ON)

    @visible.setter
    def visible(self, status):
        """Turn the display on/off (quickly)"""
        self._display_control = ByteUtil.apply_flag(self._display_control, Command.DISPLAY_ON, status)
        self.command(self._display_control)

    @property
    def cursor(self):
        """return bool: Is underline cursor visible?"""
        return ByteUtil.is_flag_active(self._display_control, Command.CURSOR_ON)

    @cursor.setter
    def cursor(self, status):
        """Turn underline cursor visibility on/off"""
        self._display_control = ByteUtil.apply_flag(self._display_control, Command.CURSOR_ON, status)
        self.command(self._display_control)

    @property
    def blink(self):
        """return bool: Is cursor blinking enabled?"""
        return ByteUtil.is_flag_active(self._display_control, Command.BLINKING_ON)

    @blink.setter
    def blink(self, status):
        """Turn blink cursor visibility on/off"""
        self._display_control = ByteUtil.apply_flag(self._display_control, Command.BLINKING_ON, status)
        self.command(self._display_control)

    @property
    def string_content(self):
        content = ''
        for row in self.content:
            for byte_char in row:
                row += chr(byte_char)
            content += '\n'

        return content

    def scroll_display_left(self):
        self.command(Command.CURSOR_OR_DISPLAY_MOVE | Command.DISPLAY_MOVE | Command.MOVE_LEFT)

    def scroll_display_right(self):
        self.command(Command.CURSOR_OR_DISPLAY_MOVE | Command.DISPLAY_MOVE | Command.MOVE_RIGHT)

    def left_to_right(self):
        """This is for text that flows Left to Right"""
        self._entry_mode |= Command.MODE_INCREMENT
        self.command(self._entry_mode)

    def right_to_left(self):
        """This is for text that flows Right to Left"""
        self._entry_mode &= ~Command.MODE_INCREMENT
        self.command(self._entry_mode)


display = lcd(db7=18, db6=15, db5=14, db4=4, rs=2, enable=3)
#display = LiquidCrystal(db7=18, db6=15, db5=14, db4=4, rs=2, enable=3)
#display2 = lcd(db7=18, db6=15, db5=14, db4=4, rs=2, enable=3)


display.write("PEDAL PI ")
display.write(" -> DIY! abcdefg", 1, 0)
time.sleep(2)

display.position = (0, 0)

for _ in range(5):
    display.scroll_display_left()
    time.sleep(0.2)

for _ in range(10):
    display.scroll_display_right()
    time.sleep(0.2)

display.home()
time.sleep(2)

display.cursor = False
display.blink = True
time.sleep(2)

display.cursor = True
display.blink = False
time.sleep(2)

display.cursor = True
display.blink = True

for row in range(2):
    for column in range(16):
        display.position = (row, column)
        time.sleep(0.1)

display.visible = False
time.sleep(2)
display.visible = True

time.sleep(2)
display.write(" Clear? ", 0, 0)
time.sleep(1)
display.clear()
display.write(" Cleared ", 1, 0)
