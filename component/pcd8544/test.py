from pcd8544 import PCD8544
from PIL import ImageFont
import time

display = PCD8544(dc=25, sclk=11, din=10, cs=8, rst=7, contrast=60, inverse=False)
#display = PCD8544(dc=25, sclk=11, din=10, cs=3, rst=2, contrast=60, inverse=False)
print(display)

# List installed fonts: fc-list
font = ImageFont.truetype('Roboto-Regular.ttf')
#font = ImageFont.load_default()
display.draw.text((10, 10), "hello", font=font, fill=1)
display.dispose()
time.sleep(0.100)

font = ImageFont.truetype('Roboto-Regular.ttf', size=15)
display.draw.text((10, 25), "world", font=font, fill=1)
display.dispose()

time.sleep(1)

display.clear()
display.dispose()

display.drawer.open("image-test.gif")
display.dispose()

time.sleep(1)

display.clear()
display.drawer.open("image-test.png")
display.dispose()

time.sleep(1)

#print("Test: Draw image.\n")
#baseName = System.getProperty("user.dir") + File.separator + "lib" \
#+ File.separator
#imageName = baseName + "pi4j-header-small3.png"
#String imageName = baseName + "test.png"

#try:
#    Image image = ImageIO.read(new File(imageName))

#    graphics.drawImage(image, 0, 0, null)
#    graphics.dispose()
#    graphics.clear()
#raise IOException e:
#    System.err.println("Possibly image was not found :/")
#    e.printStackTrace()

print("Test: Draw multiple circles.\n")
for i in range(0, 84, 4):
    coord0 = (41 - i / 2, 21 - i / 2)
    coord1 = (coord0[0] + i, coord0[1] + i)

    display.draw.ellipse([coord0, coord1], outline=1, fill=None)
    display.dispose()

display.clear()
display.dispose()

print("Test: Draw lines.\n")

for i in range(0, 84, 4):
    start_time1 = time.time()
    display.draw.line((i, 0, i, 47), fill=1)

    print(" Time to draw line: %s seconds" % (time.time() - start_time1))
    display.dispose()
    print(" Time complete to draw: %s seconds" % (time.time() - start_time1))

display.clear()

print(2)
for i in range(0, 48, 4):
    display.draw.line((0, i, 83, i), fill=1)
    display.dispose()

display.clear()

for i in range(0, 84, 4):
    print((0, 0), (i, 47))
    display.draw.line((0, 0, i, 47), fill=1)
    display.dispose()

for i in range(0, 48, 4):
    display.draw.line((0, 0, 83, i), fill=1)
    display.dispose()

display.clear()
#sleep(5000)

print("Test: Draw rectangles.\n")
for i in range(0, 48, 2):
    print((i, i), (83 - i, 47 - i))
    display.draw.rectangle(((i, i), (83 - i, 47 - i)), outline=0, fill=1)
    display.dispose()

display.clear()
#sleep(5000)

print("Test: Draw multiple rectangles.\n")
for i in range(48):
    color = 1 if i % 2 == 0 else 0
    display.draw.rectangle(((i, i), (83 - i, 47 - i)), outline=color, fill=color)
    display.dispose()

display.clear()
#sleep(5000)


#display2 = PCD8544(dc=25, sclk=11, din=10, cs=8, rst=7, contrast=60, inverse=False)
#display3 = PCD8544(dc=25, sclk=11, din=10, cs=8, rst=7, contrast=60, inverse=False)