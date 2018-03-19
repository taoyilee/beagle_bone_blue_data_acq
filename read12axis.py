import time

from app.sensors import AK8963 as msu
from app.sensors import BMP280 as baro
from app.sensors import MPU9250 as imu

MPU9250 = imu.MPU9250()
AK8963 = msu.AK8963()
BMP280 = baro.BMP280()

MPU9250.configMPU9250(imu.GFS_250, imu.AFS_8G)
AK8963.configAK8963(msu.AK8963_MODE_C100HZ, msu.AK8963_BIT_16)
while True:
    print(f"A={MPU9250.readAccel()}, G={MPU9250.readGyro()}, M={AK8963.readMagnet()}, T={MPU9250.readTemperature()} {BMP280.readPressure():.1f} hPa {BMP280.readTemperature()[0]} C")
    time.sleep(0.1)
