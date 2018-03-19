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

## Remote Interpreter Setup
### Requirements
1. Pycharm Profession License
2. Established SSH key authentication

### SSH key authentication Setup
On you PC:
```commandline
ssh-keygen
``` 
You will get .ssh/id_rsa and .ssh/id_rsa.pub (private and public key pairs). Skip this step if you already have both of them.

Copy the **public key** to beagle bone with: (Note: DO NOT copy private key. Never **EVER** do this.) 
```commandline
scp -r .ssh/id_rsa.pub <user>@<beagle_bone_IP>:~
```
Now, login to your beagle bone,
```commandline
cat ~/id_rsa.pub >> .ssh/authorized_keys
```
You now login to your beagle bone without entering password.
### Remote Interpreter Setup
1. Please follow instructions here: https://www.jetbrains.com/help/pycharm/configuring-remote-interpreters-via-ssh.html

## Beagle Bone Blue System Configuration Suggestions
### Requirements:
1. USB RJ 45 Cable
2. Micro SD Card 16GB
### OS Image Download
Beagle bone blue is compatible with beagle bone black wireless, because they both use OSD3359 SoC
Please download OS image from and follow the instructions. 
https://archlinuxarm.org/platforms/armv7/ti/beaglebone-black-wireless

It is recommended to install Archlinux to eMMC and remove SD card.

When installation is done, connect USB-RJ 45 Cable to beagle bone blue USB Type A (regular) socket. Connect beagle bone to a DHCP-enabled network and it will acquire an IP address. Login as the default user **alarm** with the password **alarm**. Business as usual afterwards.   

## Disclaimer
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## LICENSE
MIT License

Copyright (c) 2018 Michael (Tao-Yi) Lee

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

