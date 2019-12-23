#!/usr/bin/env python

########################################################################
# Author        : Labinot Rashiti
# Email         : r.labinot@gmail.com
# Date          : 15.05.2019       
# Description   : This script is used to register the LoRa module in the 
#				  IoT the network server. The script set a number of 
#				  parameters like the DevEUI, AppEUI and the AppKey.
# Requirement   : You need to put the DevEUI, AppEUI and the AppKey before
#                 starting the script.
########################################################################

# Initialization
import serial
import time

# INPUTS PARAMETERS
DEV_EUI = "XXXXXXXXXXXXXXXX"
APP_EUI = "XXXXXXXXXXXXXXXX"
APP_KEY = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

# Serial parameters to use LoRa on Microchip rn2483
SERIAL_PORT = "/dev/ttyUSB1"
BAUDRATE = 57600

# create the serial connexion with the lora module on the RaspberryPi
ser = serial.Serial(SERIAL_PORT, BAUDRATE)

# reset factory
ser.write("sys factoryRESET\r\n".encode("UTF-8"))
msg = ser.readline().decode("UTF-8").strip() # strip() delete the extra caracters
print("Reset: " + msg)

# display DevAddr
ser.write("mac get devaddr\r\n".encode("UTF-8"))
msg = ser.readline().decode("UTF-8").strip() # strip() delete the extra caracters
print("DevAddr: " + msg)

# display DevEUI
ser.write("mac get deveui\r\n".encode("UTF-8"))
msg = ser.readline().decode("UTF-8").strip() # strip() delete the extra caracters
print("DevEUI: " + msg)

# display AppEUI
ser.write("mac get appeui\r\n".encode("UTF-8"))
msg = ser.readline().decode("UTF-8").strip() # strip() delete the extra caracters
print("AppEUI: " + msg)

# set DevEUI               
ser.write(("mac set deveui " + DEV_EUI + "\r\n").encode('UTF-8'))
msg = ser.readline().decode("UTF-8").strip() # strip() delete the extra caracters
print("mac set deveui: " + msg)

# set AppEUI
ser.write(("mac set appeui " + APP_EUI + "\r\n").encode('UTF-8'))
msg = ser.readline().decode("UTF-8").strip() # strip() delete the extra caracters
print("mac set appeui: " + msg)

# set AppKey               
ser.write(("mac set appkey " + APP_KEY + "\r\n").encode('UTF-8'))
msg = ser.readline().decode("UTF-8").strip() # strip() delete the extra caracters
print("mac set appkey: " + msg)

# get the DevEUI to add in kerlink
ser.write(('mac save\r\n').encode('UTF-8'))
msg = ser.readline().decode("UTF-8").strip() # strip() delete the extra caracters
print("mac save: " + msg)

# get the DevEUI to add in kerlink
ser.write(('mac join otaa\r\n').encode('UTF-8'))
msg = ser.readline().decode("UTF-8").strip() # strip() delete the extra caracters
print("mac join: " + msg)
msg = ser.readline().decode("UTF-8").strip() # strip() delete the extra caracters
print("mac join2: " + msg)