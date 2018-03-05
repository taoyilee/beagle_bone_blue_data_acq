# coding: utf-8
import smbus
from MPU9250 import MPU9250
import time
import sys

''' MPU-9250 Register Addresses '''

## MPU9250 Default I2C slave address
MPU9250_ADDR        = 0x68
AK8963_ADDR        = 0x0C
## sample rate driver
SMPLRT_DIV     = 0x00
CONFIG         = 0x1A
GYRO_CONFIG    = 0x1B
ACCEL_CONFIG   = 0x1C
ACCEL_CONFIG_2 = 0x1D
LP_ACCEL_ODR   = 0x1E
WOM_THR        = 0x1F
FIFO_EN        = 0x23
I2C_MST_CTRL   = 0x24
I2C_MST_STATUS = 0x36
INT_PIN_CFG    = 0x37
INT_ENABLE     = 0x38
INT_STATUS     = 0x3A
ACCEL_OUT      = 0x3B
TEMP_OUT       = 0x41
GYRO_OUT       = 0x43

I2C_MST_DELAY_CTRL = 0x67
SIGNAL_PATH_RESET  = 0x68
MOT_DETECT_CTRL    = 0x69
USER_CTRL          = 0x6A
PWR_MGMT_1         = 0x6B
PWR_MGMT_2         = 0x6C
FIFO_R_W           = 0x74
WHO_AM_I           = 0x75

## Gyro Full Scale Select 250dps
GFS_250  = 0x00
## Gyro Full Scale Select 500dps
GFS_500  = 0x01
## Gyro Full Scale Select 1000dps
GFS_1000 = 0x02
## Gyro Full Scale Select 2000dps
GFS_2000 = 0x03
## Accel Full Scale Select 2G
AFS_2G   = 0x00
## Accel Full Scale Select 4G
AFS_4G   = 0x01
## Accel Full Scale Select 8G
AFS_8G   = 0x02
## Accel Full Scale Select 16G
AFS_16G  = 0x03

bus = smbus.SMBus(2)
ares = 4.0/32768.0
gres = 500.0/32768.0
# sleep off
print(f"MPS9250 = {bus.read_byte_data(MPU9250_ADDR, WHO_AM_I)}")
bus.write_byte_data(MPU9250_ADDR, PWR_MGMT_1, 0x41)
bus.write_byte_data(MPU9250_ADDR, PWR_MGMT_1, 0x01)
bus.write_byte_data(MPU9250_ADDR, PWR_MGMT_1, 0x81)
time.sleep(0.5)
bus.write_byte_data(MPU9250_ADDR, PWR_MGMT_1, 0x01)
time.sleep(0.1)
# auto select clock source
bus.write_byte_data(MPU9250_ADDR, PWR_MGMT_1, 0x01)
time.sleep(0.1)
# DLPF_CFG
bus.write_byte_data(MPU9250_ADDR, CONFIG, 0x03)
time.sleep(0.1)

bus.write_byte_data(AK8963_ADDR,  0x0B, 0x01)
bus.write_byte_data(AK8963_ADDR,  0x0A, 0x16)
print(f"AK8963 = {bus.read_byte_data(AK8963_ADDR, 0x00)}")
time.sleep(0.1)
# sample rate divider
bus.write_byte_data(MPU9250_ADDR, SMPLRT_DIV, 0x04)
# gyro full scale select
bus.write_byte_data(MPU9250_ADDR, GYRO_CONFIG, GFS_500 << 3)
# accel full scale select
bus.write_byte_data(MPU9250_ADDR, ACCEL_CONFIG, AFS_4G << 3)
# A_DLPFCFG
bus.write_byte_data(MPU9250_ADDR, ACCEL_CONFIG_2, 0x03)
# BYPASS_EN
bus.write_byte_data(MPU9250_ADDR, INT_PIN_CFG, 0x02)
time.sleep(0.1)

while True:
    print(bus.read_byte_data(MPU9250_ADDR, 0x3B),end=" ")
    print(bus.read_byte_data(MPU9250_ADDR, 0x3C),end=" ")
    print(bus.read_byte_data(MPU9250_ADDR, 0x3D),end=" ")
    print(bus.read_byte_data(MPU9250_ADDR, 0x3E),end=" ")
    print(bus.read_byte_data(MPU9250_ADDR, 0x3F),end=" ")
    print(bus.read_byte_data(MPU9250_ADDR, 0x40),end=" ")
    print(bus.read_byte_data(MPU9250_ADDR, 0x41),end=" ")
    print(bus.read_byte_data(MPU9250_ADDR, 0x42),end=" ")
    print(bus.read_byte_data(AK8963_ADDR, 0x03),end=" ")
    print(bus.read_byte_data(AK8963_ADDR, 0x04),end=" ")
    print(bus.read_byte_data(AK8963_ADDR, 0x05),end=" ")
    print(bus.read_byte_data(AK8963_ADDR, 0x06),end=" ")
    print(bus.read_byte_data(AK8963_ADDR, 0x07),end=" ")
    print(bus.read_byte_data(AK8963_ADDR, 0x08),end=" ")
    print(bus.read_byte_data(AK8963_ADDR, 0x09),end=" ")
    print("")
    time.sleep(0.5)
