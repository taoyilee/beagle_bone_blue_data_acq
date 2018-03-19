# coding: utf-8
import time

import MPU9250 as imu

MPU9250 = imu.MPU9250()
MPU9250.configMPU9250(imu.GFS_250, imu.AFS_8G)
while True:
    print(f"A={MPU9250.readAccel()}, G={MPU9250.readGyro()}")
    time.sleep(0.1)
