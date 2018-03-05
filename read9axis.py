# coding: utf-8
from MPU9250 import MPU9250
import time
import sys

mpu9250 = MPU9250()

try:
    while True:
        accel = mpu9250.readAccel()
        print(" ax = {}".format(accel['x'] ))
        print(" ay = {}".format(accel['y'] ))
        print(" az = {}".format(accel['z'] ))

        gyro = mpu9250.readGyro()
        print(" gx = {}".format( gyro['x']))
        print(" gy = {}".format( gyro['y']))
        print(" gz = {}".format( gyro['z']))

        mag = mpu9250.readMagnet()
        print(" mx = {}".format( mag['x'] ))
        print(" my = {}".format( mag['y'] ))
        print(" mz = {}".format( mag['z'] ))

        time.sleep(0.5)

except KeyboardInterrupt:
    sys.exit()
