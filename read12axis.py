import datetime
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
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    print(f"{ts:.2f} {st} MPU9250 Data: = {MPU9250.readTemperature():.1f} C ")
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    acc = MPU9250.readAccel()
    print(
        f"{ts:.2f} {st} \t{acc['x']:= 7.2f} G   {acc['y']:= 7.2f} G   {acc['z']:= 7.2f} G")
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    gyro = MPU9250.readGyro()
    print(
        f"{ts:.2f} {st} \t{gyro['x']:= 7.2f} dps {gyro['y']:= 7.2f} dps {gyro['z']:= 7.2f} dps")
    print(f"{ts:.2f} {st} AK8963 Data: = {AK8963.readMagnet()}")
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    print(f"{ts:.2f} {st} BMP280 Data: = {BMP280.readTemperature()[0]:.1f} C {BMP280.readPressure():.1f} hPa")
    time.sleep(0.5)
