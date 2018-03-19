import time

import smbus

from app.utilities import dataConv

## MPU9250 Default I2C slave address
SLAVE_ADDRESS = 0x68
## AK8963 I2C slave address
AK8963_SLAVE_ADDRESS = 0x0C
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

# AK8963 Register Addresses
AK8963_ST1 = 0x02
AK8963_MAGNET_OUT = 0x03
AK8963_CNTL1 = 0x0A
AK8963_CNTL2 = 0x0B
AK8963_ASAX = 0x10

# CNTL1 Mode select
## Power down mode
AK8963_MODE_DOWN = 0x00
## One shot data output
AK8963_MODE_ONE = 0x01

## Continous data output 8Hz
AK8963_MODE_C8HZ = 0x02
## Continous data output 100Hz
AK8963_MODE_C100HZ = 0x06

# Magneto Scale Select
## 14bit output
AK8963_BIT_14 = 0x00
## 16bit output
AK8963_BIT_16 = 0x01

## smbus
BUS_ADDRESS = 2


class AK8963:
    bus = None

    ## Constructor
    #  @param [in] address MPU-9250 I2C slave address default:0x68
    def __init__(self, address=SLAVE_ADDRESS, bus_addr=BUS_ADDRESS):
        self.bus = smbus.SMBus(bus_addr)
        self.address = address
        self.configAK8963(AK8963_MODE_C100HZ, AK8963_BIT_16)

    ## Search Device
    #  @param [in] self The object pointer.
    #  @retval true device connected
    #  @retval false device error
    def searchDevice(self):
        who_am_i = self.bus.read_byte_data(self.address, WHO_AM_I)
        return who_am_i == DEVICE_ID

    ## Configure AK8963
    #  @param [in] self The object pointer.
    #  @param [in] mode Magneto Mode Select(default:AK8963_MODE_C8HZ[Continous 8Hz])
    #  @param [in] mfs Magneto Scale Select(default:AK8963_BIT_16[16bit])
    def configAK8963(self, mode=AK8963_MODE_C100HZ, mfs=AK8963_BIT_16):
        if mfs == AK8963_BIT_14:
            self.mres = 4912.0 / 8190.0
        else:  # mfs == AK8963_BIT_16:
            self.mres = 4912.0 / 32760.0

        self.bus.write_byte_data(AK8963_SLAVE_ADDRESS, AK8963_CNTL1, 0x00)
        time.sleep(0.01)

        # set read FuseROM mode
        self.bus.write_byte_data(AK8963_SLAVE_ADDRESS, AK8963_CNTL1, 0x0F)
        time.sleep(0.01)

        # read coef data
        data = self.bus.read_i2c_block_data(AK8963_SLAVE_ADDRESS, AK8963_ASAX, 3)

        self.magXcoef = (data[0] - 128) / 256.0 + 1.0
        self.magYcoef = (data[1] - 128) / 256.0 + 1.0
        self.magZcoef = (data[2] - 128) / 256.0 + 1.0

        # set power down mode
        self.bus.write_byte_data(AK8963_SLAVE_ADDRESS, AK8963_CNTL1, 0x00)
        time.sleep(0.01)

        # set scale&continous mode
        self.bus.write_byte_data(AK8963_SLAVE_ADDRESS, AK8963_CNTL1, (mfs << 4 | mode))
        time.sleep(0.01)

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

    # Read magneto
    #  @param [in] self The object pointer.
    #  @retval x : X-magneto data
    #  @retval y : y-magneto data
    #  @retval z : Z-magneto data
    def readMagnet(self):
        x = 0
        y = 0
        z = 0

        # check data ready
        drdy = self.bus.read_byte_data(AK8963_SLAVE_ADDRESS, AK8963_ST1)
        if drdy & 0x01:
            data = self.bus.read_i2c_block_data(AK8963_SLAVE_ADDRESS, AK8963_MAGNET_OUT, 7)

            # check overflow
            if (data[6] & 0x08) != 0x08:
                x = dataConv(data[0], data[1])
                y = dataConv(data[2], data[3])
                z = dataConv(data[4], data[5])

                x = round(x * self.mres * self.magXcoef, 3)
                y = round(y * self.mres * self.magYcoef, 3)
                z = round(z * self.mres * self.magZcoef, 3)

        return {"x": x, "y": y, "z": z}
