# coding: utf-8
import time

import MPU9250 as imu

MPU9250 = imu.MPU9250()
MPU9250.configMPU9250(imu.GFS_250, imu.AFS_8G)
MPU9250.configAK8963(imu.AK8963_MODE_C100HZ, imu.AK8963_BIT_16)
while True:
    print(f"A={MPU9250.readAccel()}, G={MPU9250.readGyro()}, M={MPU9250.readMagnet()}, T={MPU9250.readTemperature()}")
    time.sleep(0.1)
