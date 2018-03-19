import time

from app.sensors import BMP280 as baro

BMP280 = baro.BMP280()
BMP280.reset()
while True:
    print(f"{BMP280.readPressure()}hPa {BMP280.readTemperature()[0]}C")
    time.sleep(0.1)
