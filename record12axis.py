import csv
import datetime
import os
import time

from app.sensors import AK8963 as msu
from app.sensors import BMP280 as baro
from app.sensors import MPU9250 as imu

MPU9250 = imu.MPU9250()
AK8963 = msu.AK8963()
BMP280 = baro.BMP280()

MPU9250.configMPU9250(imu.GFS_250, imu.AFS_8G)
AK8963.configAK8963(msu.AK8963_MODE_C100HZ, msu.AK8963_BIT_16)
ts = time.time()
st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d_%H%M%S')
output_dir = "data_collection"
os.makedirs(output_dir, exist_ok=True)

output_file = os.path.join(output_dir, f"data_12axis_{st}.csv")
print(f"** {st} Writing CSV to {output_file}")
with open(output_file, 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    csv_writer.writerow(
        ["Data", "Timestamp", "Wall_Time", "MPU_Temp", "IMU_Ax", "IMU_Ay", "IMU_Az", "IMU_Gx", "IMU_Gy",
         "IMU_Gz", "MSU_Ax", "MSU_Ay", "MSU_Az", "Baro_Temp", "Baro"])
    i = 0
    while True:
        try:
            ts = time.time()
            st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d_%H%M%S')
            temp_IMU = MPU9250.readTemperature()
            acc = MPU9250.readAccel()
            gyro = MPU9250.readGyro()
            magnet = AK8963.readMagnet()
            temp_baro = BMP280.readTemperature()[0]
            baro = BMP280.readPressure()
            csv_writer.writerow([i, ts, st, temp_IMU, acc['x'], acc['y'], acc['z'], gyro['x'], gyro['y'], gyro['z'],
                                 magnet['x'], magnet['y'], magnet['z'], temp_baro, baro])
            i += 1
        except KeyboardInterrupt:
            print(f"** {st} KeyboardInterrupt received, closing file.")
            break
