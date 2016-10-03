import time


def msleep(milliseconds):
    """Sleep the specified amount of milliseconds."""
    time.sleep(milliseconds / 1000.0)


def usleep(microseconds):
    """Sleep the specified amount of microseconds."""
    time.sleep(microseconds / 1000000.0)


class ByteUtil(object):

    @staticmethod
    def apply_flag(byte, flag, status):
        if status:
            byte |= flag
        else:
            byte &= ~flag

        return byte

    @staticmethod
    def is_flag_active(byte, flag):
        return (byte & flag) != 0
