# Copyright 2017 SrMouraSilva
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

class Command(object):
    """
    For details:
     - http://www.microcontrollerboard.com/lcd.html
     - https://www.sparkfun.com/datasheets/LCD/HD44780.pdf

    int CLEAR: Clears entire display and sets DDRAM address 0 in address counter.
    int RETURN_HOME: Sets DDRAM address 0 in address counter.
                     Also returns display from being shifted to original position.
                     DDRAM contents remain unchanged.
    int ENTRY_MODE_SET: Sets
                         - Cursor move direction - MODE_INCREMENT (left to right) or MODE_DECREMENT (right to left)
                         - Specifies display shift - ACCOPANIES_DISPLAY_SHIFT or NOT_ACCOPANIES_DISPLAY_SHIFT
                        These operations are performed during data write and read.

    int DISPLAY_ON_OFF_CONTROL: Sets
                                 - entire display on/off - DISPLAY_ON or DISPLAY_OFF
                                 - cursor on/off - CURSOR_ON or CURSOR_OFF
                                 - blinking of cursor position character (B).
    int CURSOR_OR_DISPLAY_SHIFT: Moves cursor and shifts display without changing
                                 DDRAM contents.
    int FUNCTION_SET: Sets:
                       - interface data length (DL),
                       - number of display lines - ONE_ROW or TWO_ROWS
                       - and character font - CHARACTER_5x7 or CHARACTER_5x10
    """
    CLEAR = 0x01

    RETURN_HOME = 0x02

    ENTRY_MODE_SET = 0x04
    MODE_INCREMENT = 0b0010
    MODE_DECREMENT = 0b0000
    ACCOPANIES_DISPLAY_SHIFT = 0b0001
    NOT_ACCOPANIES_DISPLAY_SHIFT = 0b0000

    DISPLAY_ON_OFF_CONTROL = 0x08
    DISPLAY_ON = 0b0100
    DISPLAY_OFF = 0b0000
    CURSOR_ON = 0b0010
    CURSOR_OFF = 0b0000
    BLINKING_ON = 0b0001
    BLINKING_OFF = 0b0000

    CURSOR_OR_DISPLAY_MOVE = 0x10
    DISPLAY_MOVE = 0b1000
    CURSOR_MOVE = 0b0000
    MOVE_RIGHT = 0b0100
    MOVE_LEFT = 0b0000

    FUNCTION_SET = 0x20
    ONE_ROW = 0b0000
    TWO_ROWS = 0b1000
    CHARACTER_5x7 = 0b0000
    CHARACTER_5x10 = 0b0100

    ROWS = [0x80, 0xC0, 0x94, 0xD4]
