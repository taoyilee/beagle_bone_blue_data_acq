#  This is a FaBo9Axis_MPU9250 library for the FaBo 9AXIS I2C Brick.
#
#  http://fabo.io/202.html
#
#  Released under APACHE LICENSE, VERSION 2.0
#
#  http://www.apache.org/licenses/
#
#  FaBo <info@fabo.io>

import time

import smbus

from app.utilities import dataConv

## MPU9250 Default I2C slave address
SLAVE_ADDRESS = 0x68

## Device id
DEVICE_ID = 0x71

''' MPU-9250 Register Addresses '''
## sample rate driver
SMPLRT_DIV = 0x00
CONFIG = 0x1A
GYRO_CONFIG = 0x1B
ACCEL_CONFIG = 0x1C
ACCEL_CONFIG_2 = 0x1D
LP_ACCEL_ODR = 0x1E
WOM_THR = 0x1F
FIFO_EN = 0x23
I2C_MST_CTRL = 0x24
I2C_MST_STATUS = 0x36
INT_PIN_CFG = 0x37
INT_ENABLE = 0x38
INT_STATUS = 0x3A
ACCEL_OUT = 0x3B
TEMP_OUT = 0x41
GYRO_OUT = 0x43

I2C_MST_DELAY_CTRL = 0x67
SIGNAL_PATH_RESET = 0x68
MOT_DETECT_CTRL = 0x69
USER_CTRL = 0x6A
PWR_MGMT_1 = 0x6B
PWR_MGMT_2 = 0x6C
FIFO_R_W = 0x74
WHO_AM_I = 0x75

## Gyro Full Scale Select 250dps
GFS_250 = 0x00
## Gyro Full Scale Select 500dps
GFS_500 = 0x01
## Gyro Full Scale Select 1000dps
GFS_1000 = 0x02
## Gyro Full Scale Select 2000dps
GFS_2000 = 0x03
## Accel Full Scale Select 2G
AFS_2G = 0x00
## Accel Full Scale Select 4G
AFS_4G = 0x01
## Accel Full Scale Select 8G
AFS_8G = 0x02
## Accel Full Scale Select 16G
AFS_16G = 0x03

## smbus
BUS_ADDRESS = 2


class MPU9250:
    bus = None

    ## Constructor
    #  @param [in] address MPU-9250 I2C slave address default:0x68
    def __init__(self, address=SLAVE_ADDRESS, bus_addr=BUS_ADDRESS):
        self.bus = smbus.SMBus(bus_addr)
        self.address = address
        self.configMPU9250(GFS_250, AFS_2G)

    ## Search Device
    #  @param [in] self The object pointer.
    #  @retval true device connected
    #  @retval false device error
    def searchDevice(self):
        who_am_i = self.bus.read_byte_data(self.address, WHO_AM_I)
        return who_am_i == DEVICE_ID

    ## Configure MPU-9250
    #  @param [in] self The object pointer.
    #  @param [in] gfs Gyro Full Scale Select(default:GFS_250[+250dps])
    #  @param [in] afs Accel Full Scale Select(default:AFS_2G[2g])
    def configMPU9250(self, gfs, afs):
        if gfs == GFS_250:
            self.gres = 250.0 / 32768.0
        elif gfs == GFS_500:
            self.gres = 500.0 / 32768.0
        elif gfs == GFS_1000:
            self.gres = 1000.0 / 32768.0
        else:  # gfs == GFS_2000
            self.gres = 2000.0 / 32768.0

        if afs == AFS_2G:
            self.ares = 2.0 / 32768.0
        elif afs == AFS_4G:
            self.ares = 4.0 / 32768.0
        elif afs == AFS_8G:
            self.ares = 8.0 / 32768.0
        else:  # afs == AFS_16G:
            self.ares = 16.0 / 32768.0

        # sleep off
        self.bus.write_byte_data(self.address, PWR_MGMT_1, 0x00)
        time.sleep(0.1)
        # auto select clock source
        self.bus.write_byte_data(self.address, PWR_MGMT_1, 0x01)
        time.sleep(0.1)
        # DLPF_CFG
        self.bus.write_byte_data(self.address, CONFIG, 0x03)
        # sample rate divider
        self.bus.write_byte_data(self.address, SMPLRT_DIV, 0x04)
        # gyro full scale select
        self.bus.write_byte_data(self.address, GYRO_CONFIG, gfs << 3)
        # accel full scale select
        self.bus.write_byte_data(self.address, ACCEL_CONFIG, afs << 3)
        # A_DLPFCFG
        self.bus.write_byte_data(self.address, ACCEL_CONFIG_2, 0x03)
        # BYPASS_EN
        self.bus.write_byte_data(self.address, INT_PIN_CFG, 0x02)
        time.sleep(0.1)

    ## brief Check data ready
    #  @param [in] self The object pointer.
    #  @retval true data is ready
    #  @retval false data is not ready
    def checkDataReady(self):
        drdy = self.bus.read_byte_data(self.address, INT_STATUS)
        if drdy & 0x01:
            return True
        else:
            return False

    ## Read accelerometer
    #  @param [in] self The object pointer.
    #  @retval x : x-axis data
    #  @retval y : y-axis data
    #  @retval z : z-axis data
    def readAccel(self):
        data = self.bus.read_i2c_block_data(self.address, ACCEL_OUT, 6)
        x = dataConv(data[1], data[0])
        y = dataConv(data[3], data[2])
        z = dataConv(data[5], data[4])

        x = round(x * self.ares, 3)
        y = round(y * self.ares, 3)
        z = round(z * self.ares, 3)

        return {"x": x, "y": y, "z": z}

    # Read gyro
    #  @param [in] self The object pointer.
    #  @retval x : x-gyro data
    #  @retval y : y-gyro data
    #  @retval z : z-gyro data
    def readGyro(self):
        data = self.bus.read_i2c_block_data(self.address, GYRO_OUT, 6)

        x = dataConv(data[1], data[0])
        y = dataConv(data[3], data[2])
        z = dataConv(data[5], data[4])

        x = round(x * self.gres, 3)
        y = round(y * self.gres, 3)
        z = round(z * self.gres, 3)

        return {"x": x, "y": y, "z": z}

    ## Read temperature
    #  @param [out] temperature temperature(degrees C)
    def readTemperature(self):
        data = self.bus.read_i2c_block_data(self.address, TEMP_OUT, 2)
        temp = dataConv(data[1], data[0])

        temp = round((temp / 333.87 + 21.0), 3)
        return temp
