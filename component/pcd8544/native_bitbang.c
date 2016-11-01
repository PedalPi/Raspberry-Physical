//gcc -shared -o native_bitbang.so -O3 -fPIC native_bitbang.c

/*
import ctypes
import numpy

lib = ctypes.cdll.LoadLibrary('./native_bitbang.so')

lib.init(ctypes.c_uint8(8), ctypes.c_uint8(9))

size = 100
array = numpy.array([i for i in range(size)]).astype(numpy.uint8)
data = array.ctypes.data

lib.bitbang_shift_out(ctypes.c_void_p(data), ctypes.c_uint32(size), ctypes.c_uint8(8), ctypes.c_uint8(9))

size = 5000
array = numpy.array([i for i in range(size)]).astype(numpy.uint8)
data = array.ctypes.data

lib.bitbang_shift_out(ctypes.c_void_p(data), ctypes.c_uint32(size), ctypes.c_uint8(8), ctypes.c_uint8(9))
*/


// https://github.com/ultibohub/Core/blob/master/source/rtl/ultibo/core/bcm2837.pas#L74
// RPI 3
#define BCM2837_PERI_BASE        0x3F000000
#define GPIO_BASE                (BCM2837_PERI_BASE + 0x200000) /* GPIO controller */

#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <sys/mman.h>
#include <unistd.h>
#include <stdint.h>

#define PAGE_SIZE (4*1024)
#define BLOCK_SIZE (4*1024)

int  mem_fd;
void *gpio_map;

// I/O access
volatile unsigned *gpio;

// GPIO setup macros. Always use INP_GPIO(x) before using OUT_GPIO(x) or SET_GPIO_ALT(x,y)
#define INP_GPIO(g) *(gpio+((g)/10)) &= ~(7<<(((g)%10)*3))
#define OUT_GPIO(g) *(gpio+((g)/10)) |=  (1<<(((g)%10)*3))
#define SET_GPIO_ALT(g,a) *(gpio+(((g)/10))) |= (((a)<=3?(a)+4:(a)==4?3:2)<<(((g)%10)*3))

#define GPIO_SET *(gpio+7)  // sets   bits which are 1 ignores bits which are 0
#define GPIO_CLR *(gpio+10) // clears bits which are 1 ignores bits which are 0

#define GET_GPIO(g) (*(gpio+13)&(1<<g)) // 0 if LOW, (1<<g) if HIGH

#define GPIO_PULL *(gpio+37) // Pull up/pull down
#define GPIO_PULLCLK0 *(gpio+38) // Pull up/pull down clock

void setup_io() {
   // open /dev/mem
   if ((mem_fd = open("/dev/mem", O_RDWR|O_SYNC) ) < 0) {
      printf("can't open /dev/mem \n");
      exit(-1);
   }

   // mmap GPIO
   gpio_map = mmap(
      NULL,                 //Any adddress in our space will do
      BLOCK_SIZE,           //Map length
      PROT_READ|PROT_WRITE, // Enable reading & writting to mapped memory
      MAP_SHARED,           //Shared with other processes
      mem_fd,               //File to map
      GPIO_BASE             //Offset to GPIO peripheral
   );

   close(mem_fd); // No need to keep mem_fd open after mmap

   if (gpio_map == MAP_FAILED) {
      printf("mmap error %d\n", (int)gpio_map); //errno also set!
      exit(-1);
   }

   // Always use volatile pointer!
   gpio = (volatile unsigned *) gpio_map;
}


//----------------------------------------

#define CLKCONST_2  400 // 400 is a good tested value for Raspberry Pi
void shift_out(uint8_t dataPin, uint8_t clockPin, uint8_t val);

void init(uint8_t dataPin, uint8_t clockPin) {
    setup_io();

    INP_GPIO(dataPin); // must use INP_GPIO before we can use OUT_GPIO
    OUT_GPIO(dataPin);

    INP_GPIO(clockPin); // must use INP_GPIO before we can use OUT_GPIO
    OUT_GPIO(clockPin);
}

void bitbang_shift_out(const void * data, uint32_t size, uint8_t dataPin, uint8_t clockPin) {
    const uint8_t * int_data = (uint8_t *) data;

    uint32_t i;
    for (i = 0; i < size; ++i)
        shift_out(dataPin, clockPin, int_data[i]);
}

/**
 * Based in http://binerry.de/post/25787954149/pcd8544-library-for-raspberry-pi
 * bitbang serial shift out on select GPIO pin. Data rate is defined by CPU clk speed and CLKCONST_2.
 * Calibrate these value for your need on target platform.*/
void shift_out(uint8_t dataPin, uint8_t clockPin, uint8_t val) {
	uint8_t i;
	uint32_t j;

	for (i = 0; i < 8; i++) {
	    if (!!(val & (1 << (7 - i))))
	        GPIO_SET = 1<<dataPin;
	    else
            GPIO_CLR = 1<<dataPin;

        GPIO_SET = 1<<clockPin;
		for (j = CLKCONST_2; j > 0; j--); // clock speed, anyone? (LCD Max CLK input: 4MHz)
		GPIO_CLR = 1<<clockPin;
	}
}
