from util.Color import Color


class PCB8544DDRamBank(object):
    '''
    Display Data Ram Bank abstraction
    See Pcd8544 datasheet for more information.
    '''
    x = 0
    y = 0
    colors = []
    changed = False

    def __init__(self, x, y, initialColor):
        self.x = x
        self.y = y

        self.changed = False
        self.colors = [initialColor] * 8

    def setPixel(self, y, color):
        if self.colors[y] != color:
            self.changed = True

        self.colors[y] = color

    def getPixel(self, y):
        return self.colors[y]

    def setChanged(self, changed):
        self.changed = changed

    def hasChanged(self):
        return self.changed

    def lsbIterator(self):
        """ @Deprecated """
        return None

    def msbIterator(self):
        return MsbIterator(self)

    @property
    def mbs_byte(self):
        index = 0
        value = 0
        for self.color in self.colors:
            value |= 0 if self.color == Color.WHITE else 1 << index
            index += 1

        return value

class MsbIterator:
    bank = None
    count = None

    def __init__(self, bank):
        """
        :param PCB8544DDRamBank bank:
        """
        self.bank = bank
        self.count = 7

    def nextElement(self):
        self.count -= 1
        return self.bank.getPixel(self.count)

    def hasNext(self):
        return self.count >= 0
