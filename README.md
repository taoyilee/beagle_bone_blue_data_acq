# beagle_bone_blue_data_acq

Beagle Bone Blue Data Acquisition is a collection of python scripts which allows owners of beagle bone blue to acquire real time sensing data from MPU9250 and AK8963 9-axis sensor.

## System Requirements
1. Python 3.6
2. Smbus python package
3. I2C-tools, and kernel headers for successful smbus installation
## Quick Start
Install smbus-cffi on your beagle bone. It is recommended to use virtual environment

```commandline
pip install smbus-cffi
``` 

Run read9axis to acquire 9-axis data dump in CLI
```commandline
python read9axis.py
```