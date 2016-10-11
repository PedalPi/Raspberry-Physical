# -*- coding: utf-8 -*-
from gpiozero import DigitalInputDevice, Button


class RotaryEncoder(object):
    """
    Decode mechanical rotary encoder pulses.

    The following example will print a Rotary Encoder change direction::

        from gpiozero import RotaryEncoder

        def change(value):
            if value > 0:
                print("clockwise")

            else:
                print("counterclockwise")

        rotary = RotaryEncoder(13, 19)
        rotary.when_rotated = change

    Based in http://abyz.co.uk/rpi/pigpio/examples.html#Python_rotary_encoder_py
    and Paul Stoffregen implementation http://www.pjrc.com/teensy/arduino_libraries/Encoder.zip

    For implementation details, access https://github.com/PedalPi/Physical/issues/1
    """
    gpio_a = None
    gpio_b = None

    old_a_value = False
    old_b_value = False

    when_rotated = lambda *args: None

    def __init__(self, pin_a, pin_b, pull_up=False):
        """
        Uses for detect rotary encoder changes (set when_rotated attribute)
        It takes one parameter which is +1 or +2 for clockwise and -1 or -2 for counterclockwise.

        :param int pin_a:
            Pin number of first (left) pin.
        :param int pin_b:
            Pin number of last (right) pin.
        :param bool pull_up:
            The common contact (middle) should be NOT connected to ground?
        """
        self.gpio_a = DigitalInputDevice(pin=pin_a, pull_up=pull_up)
        self.gpio_b = DigitalInputDevice(pin=pin_b, pull_up=pull_up)

        self.gpio_a.when_activated = self.pulse
        self.gpio_a.when_deactivated = self.pulse

        self.gpio_b.when_activated = self.pulse
        self.gpio_b.when_deactivated = self.pulse

        self.old_a_value = self.gpio_a.is_active
        self.old_b_value = self.gpio_b.is_active

        self.table_values = TableValues()

    def pulse(self):
        """
        Calls when_rotated callback if detected changes
        """
        new_b_value = self.gpio_b.is_active
        new_a_value = self.gpio_a.is_active

        value = self.table_values.value(new_b_value, new_a_value, self.old_b_value, self.old_a_value)

        self.old_b_value = new_b_value
        self.old_a_value = new_a_value

        if value != 0:
            self.when_rotated(value)


class TableValues:
    """
    Decode the rotary encoder pulse.

               +---------+         +---------+      1
               |         |         |         |
     A         |         |         |         |
               |         |         |         |
     +---------+         +---------+         +----- 0

         +---------+         +---------+            1
         |         |         |         |
     B   |         |         |         |
         |         |         |         |
     ----+         +---------+         +---------+  0

    Based in table:

    https://github.com/PedalPi/Physical/issues/1#issuecomment-248977908
    """

    def __init__(self):
        self.values = {
            0: +0,
            1: +1,
            2: -1,
            3: +2,
            # 4: -1,
            5: +0,
            6: -2,
            # 7: +1,
            # 8: +1,
            9: -2,
            10: +0,
            # 11: -1,
            12: +2,
            13: -1,
            14: +1,
            15: +0
        }

    def value(self, new_b_value, new_a_value, old_b_value, old_a_value):
        index = self.calcule_index(new_b_value, new_a_value, old_b_value, old_a_value)
        try:
            return self.values[index]
        except KeyError:
            return 0

    def calcule_index(self, new_b_value, new_a_value, old_b_value, old_a_value):
        value = 0
        if new_b_value:
            value += 8
        if new_a_value:
            value += 4
        if old_b_value:
            value += 2
        if old_a_value:
            value += 1

        return value


class RotaryEncoderWithButton(object):
    """
    Decode mechanical rotary encoder pulses.

    The following example will print a Rotary Encoder change direction::

        from gpiozero import RotaryEncoder

        def change(value):
            if value > 0:
                print("clockwise")

            else:
                print("counterclockwise")

        rotary = RotaryEncoder(13, 19)
        rotary.when_rotated = change

    Based in http://abyz.co.uk/rpi/pigpio/examples.html#Python_rotary_encoder_py
    """
    encoder = None
    button = None

    def __init__(self, pin_a, pin_b, button_pin, pull_up=False):
        """
        Rotary Encoder with Button
        Uses for detect rotary encoder changes (set when_rotated attribute)
        It takes one parameter which is +1 or +2 for clockwise and -1 or -2 for counterclockwise.

        Uses too detect button click events (set when_pressed attribute).
        If necessary use others button events, access by the button attribute

        :param int pin_a:
            Pin number of first (left) pin.
        :param int pin_b:
            Pin number of last (right) pin.
        :param int button_pin:
            Pin number of the button.
        :param bool pull_up:
            The common contacts should be NOT connected to ground?
        """
        self.encoder = RotaryEncoder(pin_a, pin_b, pull_up)
        self.button = Button(button_pin, pull_up)

    @property
    def when_rotated(self):
        return self.encoder.when_rotated

    @when_rotated.setter
    def when_rotated(self, action):
        self.encoder.when_rotated = action

    @property
    def when_pressed(self):
        return self.button.when_pressed

    @when_pressed.setter
    def when_pressed(self, action):
        self.button.when_pressed = action
