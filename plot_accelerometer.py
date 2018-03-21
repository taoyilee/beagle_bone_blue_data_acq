import datetime
import time
import matplotlib.pyplot as plt
import numpy

from app.sensors import MPU9250 as imu

MPU9250 = imu.MPU9250()

MPU9250.configMPU9250(imu.GFS_250, imu.AFS_8G)
hl, = plt.plot([], [])

while True:
    ts = time.time()
    acc = MPU9250.readAccel()
    hl.set_xdata(numpy.append(hl.get_xdata(), ts))
    hl.set_ydata(numpy.append(hl.get_ydata(), acc['x']))
    plt.draw()
    time.sleep(0.5)
