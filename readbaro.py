import time

from app.sensors import BMP280 as baro

BMP280 = baro.BMP280()

while True:
    print(f"{BMP280.readPressure()} {BMP280.readTemperature()}")
    time.sleep(0.1)
