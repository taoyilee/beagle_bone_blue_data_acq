#!/bin/bash

# 1. Please modify <USER_NAME> to your beagle bone username
# 2. Please modify <IP_ADRESS_OF_BEWAGLE_BONE> to your beagle bone IP address
# 3. Mount point defaults to ~/beaglebone/mp, create directory ~/beaglebone/mp if it is nonexistent.
#    DO NOT create mp under your local working directory.

if [ ! -d ~/beaglebone/mp ]; then
	mkdir ~/beaglebone/mp
fi
sshfs <USER_NAME>@<IP_ADDRESS_OF_BEAGLE_BONE>:. ~/beaglebone/mp -C
