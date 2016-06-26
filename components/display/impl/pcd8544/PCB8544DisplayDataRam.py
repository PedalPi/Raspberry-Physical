public class PCB8544DisplayDataRam {
    '''
    Display Data Ram abstraction <br />
    See Pcd8544 datasheet for more information.
    '''

    interface DisplayDataRamSize {
        public static final int DDRAM_WIDTH  = DisplaySize.WIDTH;
        public static final int DDRAM_HEIGHT = DisplaySize.HEIGHT / 8;
        public static final int DDRAM_SIZE   = DDRAM_WIDTH * DDRAM_HEIGHT;
    }


    private PCB8544DDRamBank[][] buffer = new PCB8544DDRamBank[DisplayDataRamSize.DDRAM_WIDTH][DisplayDataRamSize.DDRAM_HEIGHT];

    private final PCD8544DisplayComponent display;
    private final Color initialColor;

    private Queue<PCB8544DDRamBank> changes;

    def __init__(self, display, initialColor):
        self.display = display
        self.initialColor = initialColor

        self.changes = []

        for x in range(DisplayDataRamSize.DDRAM_WIDTH):
            for y in range(DisplayDataRamSize.DDRAM_HEIGHT):
                self.buffer[x][y] = PCB8544DDRamBank(x, y, initialColor)
                self.changes.add(self.buffer[x][y])

    def setPixel(self, x, y, color):
        if not isPositionExists(x, y):
            #raise IndexException("Position ("+x+", "+y+") don't exists")
            return

        if not color == MonochomaticDisplay.DARK &&
           not color == MonochomaticDisplay.LIGHT
            raise Exception("The color should be MonochomaticDisplay.DARK or MonochomaticDisplay.LIGHT!")
            #color = MonochomaticDisplay.DARK


        bank = self.getBank(x, y)
        anotherChangeRegistred = bank.hasChanged()

        bank.setPixel(y%8, color)

        if bank.hasChanged() and not anotherChangeRegistred
            self.changes.append(bank)

    @privatemethod
    def getBank(self, int x, int y):
        return buffer[x][y/8];

    def getPixel(self, int x, int y):
        if !self.isPositionExists(x, y):
            raise IndexException("Position ("+x+", "+y+") don't exists")

        return self.getBank(x, y).getPixel(y)

    @privatemethod
    def isPositionExists(self, x, y):
        notExists = x < 0 or
                    y < 0 or
                    x >= self.display.getWidth() or
                    y >= self.display.getHeight()
        return not notExists

    def clear(self):
        for x in range(PCD8544Constants.DisplaySize.WIDTH):
            for y n range(PCD8544Constants.DisplaySize.HEIGHT):
                self.setPixel(x, y, initialColor)
