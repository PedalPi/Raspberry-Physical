

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


class MsbIterator:
    PCB8544DisplayDDramBank = None
    count = None

    def __init__(self, PCB8544DisplayDDramBank):
        """
        :param PCB8544DDRamBank PCB8544DisplayDDramBank
        """
        self.PCB8544DisplayDDramBank = PCB8544DisplayDDramBank
        self.count = 7

    def next(self):
        self.count -= 1
        return self.PCB8544DisplayDDramBank.getPixel(self.count)

    def hasNext(self):
        return self.count >= 0
