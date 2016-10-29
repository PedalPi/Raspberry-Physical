//gcc -shared -o simple_pcd8544.so -O3 -fPIC -lwiringPi simple_pcd8544.c

/*
import ctypes
import numpy

lib = ctypes.cdll.LoadLibrary('./simple_pcd8544.so')

lib.init(ctypes.c_uint8(8), ctypes.c_uint8(9))

size = 100
array = numpy.array([i for i in range(size)]).astype(numpy.uint8)
data = array.ctypes.data

lib.spi_shift_out(ctypes.c_void_p(data), ctypes.c_uint32(size), ctypes.c_uint8(8), ctypes.c_uint8(9))

size = 5000
array = numpy.array([i for i in range(size)]).astype(numpy.uint8)
data = array.ctypes.data

lib.spi_shift_out(ctypes.c_void_p(data), ctypes.c_uint32(size), ctypes.c_uint8(8), ctypes.c_uint8(9))
*/

#include <wiringPi.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define CLKCONST_2  400  // 400 is a good tested value for Raspberry Pi

void shiftOut(uint8_t dataPin, uint8_t clockPin, uint8_t val);

void init(uint8_t dataPin, uint8_t clockPin) {
    wiringPiSetup();

    pinMode(dataPin, OUTPUT);
    pinMode(clockPin, OUTPUT);
}

void spi_shift_out(const void * data, uint32_t size, uint8_t dataPin, uint8_t clockPin) {
    const uint8_t * int_data = (uint8_t *) data;

    uint32_t i;
    for (i = 0; i < size; ++i)
        shiftOut(dataPin, clockPin, int_data[i]);
}

/**
 * Based in http://binerry.de/post/25787954149/pcd8544-library-for-raspberry-pi
 * bitbang serial shift out on select GPIO pin. Data rate is defined by CPU clk speed and CLKCONST_2.
 * Calibrate these value for your need on target platform.*/
void shiftOut(uint8_t dataPin, uint8_t clockPin, uint8_t val) {
	uint8_t i;
	uint32_t j;

	for (i = 0; i < 8; i++) {
		digitalWrite(dataPin, !!(val & (1 << (7 - i))));

		digitalWrite(clockPin, HIGH);
		for (j = CLKCONST_2; j > 0; j--); // clock speed, anyone? (LCD Max CLK input: 4MHz)
		digitalWrite(clockPin, LOW);
	}
}
