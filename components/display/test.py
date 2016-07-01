# -*- coding: utf-8 -*-
#from impl.TkDisplayComponent import TkDisplayComponent
from impl.PCD8544DisplayComponent import PCD8544DisplayComponent
from drawer.DisplayGraphics import DisplayGraphics

from util.Color import Color

#from time import sleep

def sleep(a):
    pass

print("Init")

# Get a display compoment
# Implemented:
#  - PCD8544: Nokia 3110 and 5110
#  - Tk: For tests in pc develop
#display = TkDisplayComponent(500, 400, True)
display = PCD8544DisplayComponent(21, 20, 16, 26, 19)


#print("Test: Display single pixel.\n")
#display.setPixel(10, 10, Color.BLACK)

# For any display changes, if you need to show the changes
# call display.redraw()
#display.redraw()


# WARNING - DisplayGraphics ignore ALL manual changes (by display.setPixel())
graphics = DisplayGraphics(display, Color.BLACK)

# Cleaning the display
#print("Clear")
#graphics.clear()

sleep(5000)

# Writting text in a (x, y) position
#graphics.drawString("Pi4j!", 0, 20)

# It's possible set the font and style usign Font:
#Font font = new Font("Serif", Font.PLAIN, 15)
#graphics.setFont(font)

# graphics.dispose is the REDRAW method
# this implementation is imcompatible with Java specification :(
# FIXME - Create a new method redraw for redraw :P
#graphics.dispose()
#graphics.clear()

sleep(5000)

# Drawing images
print("Test: Draw image.\n")
#baseName = System.getProperty("user.dir") + File.separator + "lib" \
#+ File.separator
#imageName = baseName + "pi4j-header-small3.png"
#String imageName = baseName + "test.png"

#try {
#    Image image = ImageIO.read(new File(imageName))

#    graphics.drawImage(image, 0, 0, null)
#    graphics.dispose()
#    graphics.clear()
#} catch (IOException e) {
#    System.err.println("Possibly image was not found :/")
#    e.printStackTrace()
#}

#sleep(5000)

# Line, rectangle, circle (oval) tests

print("Test: Draw many lines.\n")
for i in range(0, 84, 4):
    graphics.canvas.create_line(0, 0, i, 47)
    graphics.dispose()

for i in range(0, 48, 4):
    graphics.canvas.create_line(0, 0, 83, i)
    graphics.dispose()

graphics.clear()
sleep(5000)

print("Test: Draw rectangles.\n")
for i in range(0, 48, 2):
    graphics.drawRect(i, i, 83 - i, 47 - i)
    graphics.dispose()

graphics.clear()
sleep(5000)

print("Test: Draw multiple rectangles.\n")
for i in range(48):
    color = Color.BLACK if i % 2 == 0 else Color.WHITE
    graphics.setColor(color)
    graphics.fillRect(i, i, 83 - i, 47 - i)
    graphics.dispose()

graphics.clear()
sleep(5000)


print("Test: Draw multiple circles.\n")
graphics.setColor(Color.BLACK)
for i in range(0, 48, 6):
    graphics.drawOval(41 - i / 2, 41 - i / 2, i, i)
    graphics.dispose()


graphics.clear()
sleep(5000)
