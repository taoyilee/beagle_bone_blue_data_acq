from smbus import SMBus
import os
# import numpy as np

import time

''' MPU9250 Default I2C slave address '''
MPU9250_ADDR = 0x68

''' MPU-9250 Register Addresses '''
ACCEL_CONFIG = 0x1C
ACCEL_XOUT_H = 0x3B
ACCEL_XOUT_L = 0x3C
ACCEL_YOUT_H = 0x3D
ACCEL_YOUT_L = 0x3E
ACCEL_ZOUT_H = 0x3F
ACCEL_ZOUT_L = 0x40
PWR_MGMT_1 = 0x6B

''' ACCEL_CONFIG Setting '''
ACCEL_FSR_CFG_2G = 0x00 << 3
ACCEL_FSR_CFG_4G = 0x01 << 3
ACCEL_FSR_CFG_8G = 0x02 << 3
ACCEL_FSR_CFG_16G = 0x03 << 3

''' PWR_MGMT_1 Setting '''
H_RESET = (0x01 << 7)

''' Here we go '''
bus = SMBus(2)

bus.write_byte_data(MPU9250_ADDR, PWR_MGMT_1, H_RESET)
time.sleep(1)

bus.write_byte_data(MPU9250_ADDR, ACCEL_CONFIG, ACCEL_FSR_CFG_2G)
ACCEL_TO_MS2 = 9.80665 * 2.0 / 32768.0
time.sleep(1)

while True:
    acc_x_high = bus.read_byte_data(MPU9250_ADDR, ACCEL_XOUT_H)
    acc_x_low = bus.read_byte_data(MPU9250_ADDR, ACCEL_XOUT_L)
    acc_x_raw = (acc_x_high << 8) | acc_x_low

    acc_y_high = bus.read_byte_data(MPU9250_ADDR, ACCEL_YOUT_H)
    acc_y_low = bus.read_byte_data(MPU9250_ADDR, ACCEL_YOUT_L)
    acc_y_raw = (acc_y_high << 8) | acc_y_low

    acc_z_high = bus.read_byte_data(MPU9250_ADDR, ACCEL_ZOUT_H)
    acc_z_low = bus.read_byte_data(MPU9250_ADDR, ACCEL_ZOUT_L)
    acc_z_raw = (acc_z_high << 8) | acc_z_low
    # print('x acc raw = %d' % (acc_x_raw))
    print('x acc m/s^2 = %.2f' % (acc_x_raw * ACCEL_TO_MS2))
    print('y acc m/s^2 = %.2f' % (acc_y_raw * ACCEL_TO_MS2))
    print('z acc m/s^2 = %.2f' % (acc_z_raw * ACCEL_TO_MS2))
    # print(chr(27) + "[2J")
