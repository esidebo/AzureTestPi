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
import traceback
# import json
# import requests


successCount = 0 # not needed in production. Used for script testing.
failureCount = 0 # not needed in production. Used for script testing.
exceptionCount = 0 # not needed in production. Used for script testing.
startTime = time.time()

# Set the up required variables for Azure Iot Hub
AzureDeviceName = "TestPi"
AzureDeviceKey = "1Hfen5Do2lS+RgtCe8RftdfqzmpgmMbXOj0i8ucEk+A="
AzureHubName = "SPMOilMonitor"
sasTimeOut = 86400 #24 hours

# Create the device object and get the initial sas
device = Device.Device(AzureHubName.lower(), AzureDeviceName, AzureDeviceKey)
device.create_sas(sasTimeOut)
print('Initial sas created: ' + device._sas)

print('Started at: ' + str(datetime.datetime.utcnow()) + '  in seconds: ' + str(time.time()))

while True:
	# Acquire and format the time stamp
	timeStamp = datetime.datetime.utcnow()
	timeStamp_str = timeStamp.strftime('%Y-%m-%dT%H:%M:%S.%fZ')

	# Acquire the CPU core temperature
	temp = int(open('/sys/class/thermal/thermal_zone0/temp').read()) / 1e3

	# Create the data string
	data = {'TimeStamp' : timeStamp_str, 'CPUTemp' : temp}

	# calculate time since sas was created
	currentTime = time.time()
	timeElapsed = currentTime - startTime

	# Create new sas if old one has expired
	if timeElapsed > sasTimeOut:
		device.create_sas(sasTimeOut)
		print(timeStamp_str + '; Created new SAS: ' + device._sas)
		startTime = currentTime

	# Send the data to Azure
	try:
		AzureSender = device.send(data)
	except Exception as e:
		print(timeStamp_str + '; Exception: %s' % e)
		exceptionCount += 1
		print('Success Count: ' + str(successCount) + '; Failure Count: ' + str(failureCount) + '; Exception Count: ' + str(exceptionCount))
		pass

	# Check for valid transmission
	if AzureSender == 204: # Successful Post
		successCount += 1

	elif AzureSender == 401: # Failed Authorization - Redo sas
		failureCount += 1
		print(timeStamp_str + '; Error Code: ' + str(AzureSender) + '; Create new sas')
		device.create_sas(sasTimeOut)
		print('New sas: ' + device._sas)
		print('Success Count: ' + str(successCount) + '; Failure Count: ' + str(failureCount) + '; Exception Count: ' + str(exceptionCount))
	
	else: # Failed transmission, record code
		failureCount += 1
		print(timeStamp_str + '; Error Code: ' + str(AzureSender))
		print('Success Count: ' + str(successCount) + '; Failure Count: ' + str(failureCount) + '; Exception Count: ' + str(exceptionCount))
		
	# print(timeStamp_str + '; Success Count: ' + str(successCount) + '; Failure Count: ' + str(failureCount))
	time.sleep(30) # 1Hz upload rate
