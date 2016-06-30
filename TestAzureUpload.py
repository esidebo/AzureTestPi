# !/home/pi
import sys
import DeviceClient
import Device
import time
import datetime
import json
import requests

successCount = 0
failureCount = 0
while True:
	# Set the up required variables for Azure Iot Hub
	AzureDeviceName = "YourDeviceName"
	AzureDeviceKey = "YourDeviceKey"
	AzureHubName = "YourAzureIoTHubName"

	# while True:
	# Acquire and format the time stamp
	timeStamp = datetime.datetime.utcnow()
	timeStamp_str = timeStamp.strftime('%Y-%m-%dT%H:%M:%S.%fZ')

	# Acquire the CPU core temperature
	temp = int(open('/sys/class/thermal/thermal_zone0/temp').read()) / 1e3

	# # Create the JSON message
	# JsonMessage = json.dumps({'TimeStamp' : timeStamp_str, 'CPUTemp' : temp})
	# print('Message to Send:' + JsonMessage)

	# Create the data
	data = {'TimeStamp' : timeStamp_str, 'CPUTemp' : temp}
	print('Data: ' + str(data))

	# Send the data to Azure
	device = Device.Device(AzureHubName.lower(), AzureDeviceName, AzureDeviceKey)
	print('Initialized Device')
	print('Base url: ' + device._base_url)
	device.create_sas(600)
	print ('Created SAS: ' + device._sas)

	AzureSender = device.send(data)
	if AzureSender == 204:
		successCount += 1
		print('Success')
	else:
		print('Failure')
		failureCount += 1

	print('Success Count: ' + str(successCount) + '   Failure Count: ' + str(failureCount))
	time.sleep(30)
