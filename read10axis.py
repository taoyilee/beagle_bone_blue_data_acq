import time

from app.sensors import MPU9250 as imu
from app.sensors import AK8963 as msu

MPU9250 = imu.MPU9250()
AK8963 = msu.AK8963()

MPU9250.configMPU9250(imu.GFS_250, imu.AFS_8G)
AK8963.configAK8963(msu.AK8963_MODE_C100HZ, msu.AK8963_BIT_16)
while True:
    print(f"A={MPU9250.readAccel()}, G={MPU9250.readGyro()}, M={AK8963.readMagnet()}, T={MPU9250.readTemperature()}")
    time.sleep(0.1)
