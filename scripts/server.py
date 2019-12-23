#!/usr/bin/env python3

########################################################################
# Author        : Labinot Rashiti
# Email         : r.labinot@gmail.com
# Date          : 24.06.2019
# Description   : This script is used to launch a HTTP server that will
#                 receive the data and save it in the influxDB.
########################################################################

# IMPORT FOR THE RECEIVING DATA AND PARSING
from flask import Flask, request, Response
import binascii
import traceback
import struct

# IMPORT FOR THE SENDING DATA TO InfluxDB
from influxdb import InfluxDBClient
import datetime
import pytz
import requests

HOST = "localhost"
PORT = 8086
USER = "root"
PASSWORD = "root"
DATABASE = "iotawater"

# create the connexion with InfluxDB
client = InfluxDBClient(HOST, PORT, USER, PASSWORD, DATABASE)

app = Flask(__name__)

# default route for the kerlink to send data
@app.route('/rxmessage', methods=["POST"])
def index():
        # get the json body
        jsonBody = request.get_json()

        # extract the payload
        payload = jsonBody['userdata']['payload']

        # extract the specific type and ID of the device
        deviceType = payload[:2]
        deviceID = payload[2:4]

        # Check if it is a water type device
        if (deviceType == "01"):
                # extract only the flow rate data in hex
                deviceData = payload[4:]
                print("deviceData as hex: " + deviceData)

                # Transform hex string to bytes
                deviceData = bytes(deviceData, encoding="utf-8")
                print("deviceData as bytes : " + str(deviceData))
				
                # Transform the bytes to float value
                deviceData = binascii.unhexlify(deviceData)
                (flowRate,) = struct.unpack('<f', deviceData)
                flowRate = float("{0:.3f}".format(flowRate))
                print("flow rate : " + str(flowRate))


        # datetime doesn't give a standard date time with UTC timezone, so we add it
        timestamp = datetime.datetime.utcnow()
        timestamp = timestamp.replace(tzinfo=pytz.utc)
        print("time :" + str(timestamp))

        # Preparing the request to InfluxDB
        requestInfluxDB = [
                {
                        "measurement": "floorB",
                        "tags": {
                        },
                        "time": str(timestamp),
                        "fields": {
                            "flowRate": flowRate
                        }
                }
        ]

        # Store the flow rate and send back a good HTTP status
        client.write_points(requestInfluxDB)
        return Response("{'a':'b'}", status=201, mimetype='application/json')


# init
if __name__ == "__main__":
        app.run(host="0.0.0.0", port=9999)
