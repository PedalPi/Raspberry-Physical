from gpiozero import LED
from component.sevensegments.seven_segments_dictionary import dictionary
from component.sevensegments.multiplex_thread import MultiplexThread
from component.sevensegments.display_strategy import CommonStrategy, NotCommonStrategy
from component.sevensegments.text_write_strategy import TextWriteStrategy


class SevenSegmentsBoard(object):
    pins = []

    def __init__(self, a, b, c, d, e, f, g):
        self.pins = [
            LED(a),
            LED(b),
            LED(c),
            LED(d),
            LED(e),
            LED(f),
            LED(g)
        ]

        self.displays = []
        self._value = ''
        self._thread = None

        self._status = True

    def add_display(self, common=None, anode=False):
        display = SevenSegmentsDisplay(
            self.pins[0],
            self.pins[1],
            self.pins[2],
            self.pins[3],
            self.pins[4],
            self.pins[5],
            self.pins[6],
            common=common,
            anode=anode
        )

        self.displays.append(display)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, text):
        if self._thread is not None:
            self._thread.stop()

        self._value = TextWriteStrategy.prepare_text(len(self.displays), text)

        for character, display in zip(self._value, self.displays):
            display.value = character

        if len(self.displays) > 1:
            self._thread = MultiplexThread(self)
            self._thread.start()

    def off(self):
        if not self._status:
            return

        self._status = False

        if self._thread is not None:
            print('stopped')
            self._thread.stop()

        for display in self.displays:
            display.off()

    def on(self):
        if self._status:
            return

        self._status = True

        for display in self.displays:
            display.on()

    def register(self, char_symbol, byte):
        """
        Link a char_symbol with a byte. The byte represents a led state

        :param char_symbol: if
        :param byte: Each bit represents a led state
                     In order: 1º MSB is ``a led``,
                               2º MSB is ``b led``,
                               consecutively
                               The LCB is dot ``led``;
        """
        dictionary[char_symbol] = byte


class SevenSegmentsDisplay(object):

    def __init__(self, a, b, c, d, e, f, g, common=None, anode=False):
        self.pins = [a, b, c, d, e, f, g]

        self.anode = anode

        self._value = ' '
        self._status = None

        self.strategy = CommonStrategy(self, common) if common is not None else NotCommonStrategy()
        self.common = common

        self.on()

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, status):
        self._status = status

        if status:
            self.on()
        else:
            self.off()

    def on(self):
        if self.status:
            return

        self._status = True
        self.strategy.on()

    def off(self):
        if not self.status:
            return

        self._status = False
        self.strategy.off()

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if value not in dictionary:
            raise KeyError('Symbol not registered: ' + value)

        self._value = value

        if self.status:
            self._write(value)

    def _write(self, value):
        character = self._char_pins(value)
        comparator = 0b10000000

        for i in range(7):
            light = (comparator & character) == comparator
            self.pins[i].value = light

            comparator >>= 1

    def _char_pins(self, char):
        character = dictionary[char]

        if not self.anode:
            character = ~character

        return character

    def _rewrite(self):
        """
        Write (again) the last character displayed
        It is used in multiplex displays
        """
        self.strategy.rewrite()

'''
board = SevenSegmentsBoard(a=13, b=6, c=16, d=20, e=21, f=19, g=26)

board.add_display(common=5, anode=False)
board.add_display(common=1, anode=True)


import time

for i in range(2):
    board.value = i
    print(board.value, i)
    time.sleep(2)

board.register('~', 0b10101010)
board.value = '~~'

time.sleep(2)

board.off()
'''