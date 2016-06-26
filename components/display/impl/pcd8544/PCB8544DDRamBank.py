

class PCB8544DDRamBank(self):
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

        self.changed = false
        self.colors = [initialColor] * 8

    def setPixel(self, y, color):
        if self.colors[y] != color:
            self.changed = True

        self.colors[y] = color

    def getPixel(self, y):
        return colors[y]

    def setChanged(self, changed):
        self.changed = changed

    def hasChanged(self):
        return this.changed;

    /**
     * @deprecated It's not necessary
     */
    @Deprecated
    public Iterator<Color> lsbIterator() {
        return null;
    }
    
    public Iterator<Color> msbIterator() {
        return new MsbIterator(this);
    }

    private static class MsbIterator implements Iterator<Color> {
        private PCB8544DDRamBank PCB8544DisplayDDramBank;
        private int count;

        public MsbIterator(PCB8544DDRamBank PCB8544DisplayDDramBank) {
            this.PCB8544DisplayDDramBank = PCB8544DisplayDDramBank;
            this.count = 7;
        }

        @Override
        public Color next() {
            return PCB8544DisplayDDramBank.getPixel(count--);
        }

        @Override
        public boolean hasNext() {
            return count >= 0;
        }
    }
}
