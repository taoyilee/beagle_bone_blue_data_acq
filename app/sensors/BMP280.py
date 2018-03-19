# MIT License
#
# Copyright (c) 2018 Michael (Tao-Yi) Lee
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import time

import smbus

from app.utilities import dataConv_20bit

SLAVE_ADDRESS = 0x76
DEVICE_ID = 0x58
BUS_ADDRESS = 2

MODE_SLP = 0b00
MODE_FRC = 0b01
MODE_NRM = 0b11

TEMP_XLSB = 0xFC
TEMP_LSB = 0xFB
TEMP_MSB = 0xFA
PRESS_XLSB = 0xF9
PRESS_LSB = 0xF8
PRESS_MSB = 0xF7
CONFIG = 0xF5
CTRL_MEAS = 0xF4
STATUS = 0xF3
RESET = 0xE0
WHO_AM_I = 0xD0

DIG_T1_L = 0x88  # unsigned short
DIG_T1_M = 0x89
DIG_T2_L = 0x8A  # signed short
DIG_T2_M = 0x8B
DIG_T3_L = 0x8C  # signed short
DIG_T3_M = 0x8D

DIG_P1_L = 0x8E  # unsigned short
DIG_P1_M = 0x8F
DIG_P2_L = 0x90  # signed short
DIG_P2_M = 0x91
DIG_P3_L = 0x92  # signed short
DIG_P3_M = 0x93
DIG_P4_L = 0x94  # signed short
DIG_P4_M = 0x95
DIG_P5_L = 0x96  # signed short
DIG_P5_M = 0x97
DIG_P6_L = 0x98  # signed short
DIG_P6_M = 0x99
DIG_P7_L = 0x9A  # signed short
DIG_P7_M = 0x9B
DIG_P8_L = 0x9C  # signed short
DIG_P8_M = 0x9D
DIG_P9_L = 0x9E  # signed short
DIG_P9_M = 0x9F

SPI = 0b0  # Disable SPI
IIR_OFF = 0b000
IIR_COEFF_2 = 0b001
IIR_COEFF_4 = 0b010
IIR_COEFF_8 = 0b011
IIR_COEFF_16 = 0b100

T_SB_0p5MS = 0b000
T_SB_62p5MS = 0b001
T_SB_125MS = 0b010
T_SB_250MS = 0b011
T_SB_500MS = 0b100
T_SB_1000MS = 0b101
T_SB_2000MS = 0b110
T_SB_4000MS = 0b111

OVERSAMPLING_P_SKIP = 0b000
OVERSAMPLING_P_1 = 0b001
OVERSAMPLING_P_2 = 0b010
OVERSAMPLING_P_4 = 0b011
OVERSAMPLING_P_8 = 0b100
OVERSAMPLING_P_16 = 0b101

OVERSAMPLING_T_SKIP = 0b000
OVERSAMPLING_T_1 = 0b001
OVERSAMPLING_T_2 = 0b010
OVERSAMPLING_T_4 = 0b011
OVERSAMPLING_T_8 = 0b100
OVERSAMPLING_T_16 = 0b101


class BMP280:
    bus = None

    def __init__(self, address=SLAVE_ADDRESS, bus_addr=BUS_ADDRESS):
        self.bus = smbus.SMBus(bus_addr)
        self.address = address
        self.configBMP280()

    def searchDevice(self):
        who_am_i = self.bus.read_byte_data(self.address, WHO_AM_I)
        return who_am_i == DEVICE_ID

    def reset(self):
        self.bus.write_byte_data(self.address, RESET, 0xB6)
        time.sleep(0.1)

    def configBMP280(self, ovs_p=OVERSAMPLING_P_16, ovs_t=OVERSAMPLING_T_16, iir=IIR_OFF, t_sb=T_SB_0p5MS, spi=SPI):
        # sleep off
        self.bus.write_byte_data(self.address, CTRL_MEAS, ovs_t << 5 | ovs_p << 2 | MODE_NRM)
        time.sleep(0.1)

        # config
        self.bus.write_byte_data(self.address, CTRL_MEAS, t_sb << 5 | iir << 2 | spi)
        time.sleep(0.1)

    def readPressure(self):
        data = self.bus.read_i2c_block_data(self.address, PRESS_MSB, 3)
        return dataConv_20bit(data_msb=data[0], data_lsb=data[1], data_xlsb=data[2])

    def readTemperature(self):
        data = self.bus.read_i2c_block_data(self.address, TEMP_MSB, 3)
        return dataConv_20bit(data_msb=data[0], data_lsb=data[1], data_xlsb=data[2])
