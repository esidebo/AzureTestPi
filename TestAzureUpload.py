"""
    A simple implementation of Azure IoT Hub REST APIs to 
    upload data from a Raspberry Pi to the Azure IoT Hub.
"""
# !/home/pi
import sys
# import DeviceClient
import Device
import time
import datetime
# import json
# import requests


successCount = 0 # not needed in production. Used for script testing.
failureCount = 0 # not needed in production. Used for script testing.
startTime = time.time()

# Set the up required variables for Azure Iot Hub
AzureDeviceName = "TestPi"
AzureDeviceKey = "1Hfen5Do2lS+RgtCe8RftdfqzmpgmMbXOj0i8ucEk+A="
AzureHubName = "SPMOilMonitor"
sasTimeOut = 86400 # 24 hours

# Create the device object
device = Device.Device(AzureHubName.lower(), AzureDeviceName, AzureDeviceKey)
# print('Initialized Device object')
# print('Base url: ' + device._base_url)
device.create_sas(sasTimeOut)
print('Initial sas created: ' + device._sas)

print('Started at: ' + str(datetime.datetime.utcnow()) + '  in seconds: ' + str(time.time()))

while failureCount < 1:
	# Acquire and format the time stamp
	timeStamp = datetime.datetime.utcnow()
	timeStamp_str = timeStamp.strftime('%Y-%m-%dT%H:%M:%S.%fZ')

	# Acquire the CPU core temperature
	temp = int(open('/sys/class/thermal/thermal_zone0/temp').read()) / 1e3

	# Create the data string
	data = {'TimeStamp' : timeStamp_str, 'CPUTemp' : temp}
	# print('Data: ' + str(data))
	currentTime = time.time()
	timeElapsed = currentTime - startTime
	# print('Time Elapsed: ' + str(timeElapsed))

	if timeElapsed > sasTimeOut:
		device.create_sas(sasTimeOut)
		print(timeStamp_str + '; Created new SAS: ' + device._sas)
		startTime = currentTime

	AzureSender = device.send(data)
	if AzureSender == 204:
		successCount += 1
		# print('Successful Upload')
	else:
		# print('Failure')
		failureCount += 1
		print('Failed at: ' + str(datetime.datetime.utcnow()) + '  in seconds: ' + str(time.time()))
		# print('Old Sas: ' + device._sas)
		# device.create_sas(sasTimeOut)
		# print('New sas: ' + device._sas)


	# print(timeStamp_str + '; Success Count: ' + str(successCount) + '; Failure Count: ' + str(failureCount))
	time.sleep(60) # 1Hz upload rate
