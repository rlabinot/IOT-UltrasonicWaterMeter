#!/usr/bin/env python3

########################################################################
# Author        : Labinot Rashiti
# Email         : r.labinot@gmail.com
# Date          : 01.07.2019       
# Description   : This script is used to read the data water flow from 
#                 a TUF-2000B sensor and send it to the IOT network server.
########################################################################

import minimalmodbus # minimalmodbus is a library for serial communication
import binascii # binascii is a library for type conversion
import serial # serial for LoRa Module communication
import struct # pack the float data
import time # to make the script sleep for 5 minutes

# TUF-2000B CONFIGURATION
TUF_BAUDRATE = 9600
TUF_SERIAL_PORT = "/dev/ttyUSB0"
TUF_SLAVE_ADDRESS = 1

# LOSTIK CONFIGURATION
LOSTIK_BAUDRATE = 57600
LOSTIK_SERIAL_PORT = "/dev/ttyUSB1"

# Informations about the device for LoRa
DEVICE_TYPE = "01"
DEVICE_ID = "01"

# connection with the TUF-2000B with the slaveaddress = 1. By default, it is in Modbus RTU mode
instrument = minimalmodbus.Instrument(TUF_SERIAL_PORT, TUF_SLAVE_ADDRESS)
# edit the default parameters to be compatile with TUF-2000B
instrument.serial.baudrate = TUF_BAUDRATE

# connection with the LoRa module LoStik on the RaspberryPi
ser = serial.Serial(LOSTIK_SERIAL_PORT, LOSTIK_BAUDRATE)


def getFlowRate(register):
    try:
        # read the daily flow rate in m3 in the register n°125 (from the TUF-2000B registry board PDF)
        output = instrument.read_float(register)
        output = float("{0:.3f}".format(output))
        
		# check if the daily value has been reset
        if (output < 0):
            output = 0
        
        return output
    except:
        print("There is an error reading the flow rate request")


def sendDataLoRa(payload):
    try:
        command = "mac tx uncnf 1 " + payload +"\r\n"
        ser.write(command.encode("UTF-8"))
        msg = ser.readline().decode("UTF-8").strip() # strip() delete the extra caracters
        msg = ser.readline().decode("UTF-8").strip() # strip() delete the extra caracters
        return True
    except:
        print("There is an error with the LoRa communication")
        return False


def main():
    # initialise the first value reference
    currentFlowRate = getFlowRate(125)
    while True:

        # get the flow rate from the TUF-2000B
        flowRate = getFlowRate(125)
        
        if (flowRate < currentFlowRate):
            # Daily update
            currentFlowRate = flowRate

        hexValue = struct.pack('<f', flowRate) # compact the float
        hexValue = binascii.hexlify(hexValue) # convert to hex
        hexValue = str(hexValue)[2:-1] # extract only the hex part as string hex for the LoRa command
    
        # Build the frame to send with LoRa by adding the type and ID of the device
        dataToSend = DEVICE_TYPE + DEVICE_ID + hexValue
        sendDataLoRa(dataToSend)
        print("Data has been sent")
        time.sleep(300)

main()
