class PCD8544DisplayComponent(MochromaticDisplay):
    '''
    PCD8544 display implementation.

    This implementation uses software shiftOut implementation

    @author SrMouraSilva
    Based in 2013 Giacomo Trudu - wicker25[at]gmail[dot]com
    Based in 2010 Limor Fried, Adafruit Industries https://github.com/adafruit/Adafruit_Nokia_LCD/blob/master/Adafruit_Nokia_LCD/PCD8544.py
    Based in CORTEX-M3 version by Le Dang Dung, 2011 LeeDangDung@gmail.com (tested on LPC1769)
    Based in Raspberry Pi version by Andre Wussow, 2012, desk@binerry.de
    Based in Raspberry Pi Java version by Cleverson dos Santos Assis, 2013, tecinfcsa@yahoo.com.br
    '''

    #private static final int CLOCK_TIME_DELAY = 1;//micro seconds // 10 nanosseconds is the correct 
    #http://stackoverflow.com/questions/11498585/how-to-suspend-a-java-thread-for-a-small-period-of-time-like-100-nanoseconds
    RESET_DELAY = 1 #10^-3ms is the correct

    DDRAM = None

    ''' Serial data input '''
    DIN = None
    ''' Input for the clock signal '''
    SCLK = None
    ''' Data/Command mode select '''
    DC = None
    ''' External rst input '''
    RST = None
    ''' Chip Enable (CS/SS) '''
    SCE = None

    def __init__(
            GpioPinDigitalOutput din, 
            GpioPinDigitalOutput sclk, 
            GpioPinDigitalOutput dc, 
            GpioPinDigitalOutput rst,
            GpioPinDigitalOutput cs,

            byte contrast,
            boolean inverse):
        '''
        @param din Serial data input.
        @param sclk Input for the clock signal.
        @param dc Data/Command mode select.
        @param rst External rst input.
        @param cs Chip Enable (CS/SS)

        @param contrast
        @param inverse
        '''
        self.DDRAM = PCB8544DisplayDataRam(self, Color.WHITE);

        self.DIN = din
        self.SCLK = sclk
        self.DC = dc
        self.RST = rst
        self.SCE = cs

        self.reset()
        self.init(contrast, inverse)
        self.redraw()

    @privatemethod
    def reset(self):
        self.RST.low()
        try:
            Thread.sleep(RESET_DELAY)
        catch InterruptedException e:
            e.printStackTrace()

        self.RST.high()

    @privatemethod
    def init(self, contrast, inverse):
        self.sendCommands(SysCommand.FUNC, Setting.FUNC_H)
        self.sendCommands(SysCommand.BIAS, new ByteCommand(0x04))
        self.sendCommands(SysCommand.VOP, new ByteCommand(contrast & 0x7f ))
        self.sendCommand(SysCommand.FUNC);
        self.sendCommands(
            SysCommand.DISPLAY,
            Setting.DISPLAY_D,
            new ByteCommand(Setting.DISPLAY_E.cmd() * (byte) (inverse ? 1 : 0))
        )

    @privatemethod
    def sendCommands(self, Command ... commands):
        '''
        @param Send command | command | command
        '''
        self.sendCommand(Command.generateBy(commands))

    @privatemethod
    def sendCommand(self, data):
        self.DC.low()

        self.SCE.low()
        self.writeData(data)
        self.SCE.high()

    @privatemethod
    def writeData(data):
    	DataTransmitionUtil.shiftOut(data, DIN, SCLK, BitOrderFirst.MSB)

    @privatemethod
    def toggleClock(self):
        self.SCLK.high()
        # The pin changes usign wiring pi are 20ns?
        # The pi4j in Snapshot 1.1.0 are 1MHz ~ 1 microssecond in Raspberry 2      http://www.savagehomeautomation.com/projects/raspberry-pi-with-java-programming-the-internet-of-things-io.html#follow_up_pi4j
        # Its necessary only 10ns    Pag 22 - https://www.sparkfun.com/datasheets/LCD/Monochrome/Nokia5110.pdf
        # Not discoment :D
        #Gpio.delayMicroseconds(CLOCK_TIME_DELAY);
        self.SCLK.low()

    @privatemethod
    def setContrast(self, value):
        self.sendCommand(SysCommand.FUNC, Setting.FUNC_H)
        self.sendCommand(SysCommand.VOP, new ByteCommand(value & 0x7f))
        self.sendCommand(SysCommand.FUNC)

    def setPixel(self, x, y, color):
        self.DDRAM.setPixel(x, y, color)    

    def getPixel(self, x, y):
        return self.DDRAM.getPixel(x, y)

    def redraw(self):
        Queue<PCB8544DDRamBank> changes = self.DDRAM.getChanges()
        while not changes.isEmpty():
            bank = changes.remove()
            self.setCursorY(bank.y())
            self.setCursorX(bank.x())

            self.sendData(bank)

    @privatemethod
    def sendData(self, PCB8544DDRamBank bankData):
        self.DC.high()

        self.SCE.low()
        self.writeData(bankData)
        self.SCE.high()

    @privatemethod
    def writeData(self, bank):
        Iterator<Color> iterator = bank.msbIterator()
        while iterator.hasNext():
            Color color = iterator.next()
            DIN.setState(color.equals(Color.BLACK) ? True : False)

            self.toggleClock()

        bank.setChanged(False)

    @privatemethod
    def setCursorX(self, x):
        self.sendCommand(SysCommand.XADDR, new ByteCommand(x))

    @privatemethod
    def setCursorY(self, y):
        self.sendCommand(SysCommand.YADDR, new ByteCommand(y))

    def clear(self):
        self.DDRAM.clear()

        self.setCursorX(0)
        self.setCursorY(0)

    def getWidth(self):
        return DisplaySize.WIDTH

    def getHeight(self):
        return DisplaySize.HEIGHT
