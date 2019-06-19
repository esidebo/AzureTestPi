"""
    A simple implementation of Azure IoT Hub REST APIs to
    upload data from a Raspberry Pi to the Azure IoT Hub.
"""
# !/home/pi
import sys
# import DeviceClient
import Cloud
import time
import datetime
import traceback
# import json
# import requests

successCount = 0 # not needed in production. Used for script testing.
failureCount = 0 # not needed in production. Used for script testing.
exceptionCount = 0 # not needed in production. Used for script testing.
startTime = time.time()

MSG_INTERVAL_SEC = 5

HUB_KEY = "Q258tmmhnXPSAyKpcO6WexM4DATgb8cnhz63WMtsa0M="

# Set the up required variables for Azure Iot Hub
AzureDeviceName = "MimeRacer"
AzureDeviceKey = "Le+4jMDLInzRQ68bFel+uDaGAfVBKD0rz7qRBaVY/IM="
AzureHubName = "iothub-kistamobweek"
sasTimeOut = 86400 #24 hours

# Create the cloud object and get the initial sas
cloud = Cloud.Cloud(AzureHubName.lower(), AzureDeviceName, AzureDeviceKey)
cloud.create_sas(HUB_KEY, 'iothubowner', sasTimeOut)
print('Initial sas created: ' + cloud._sas)

print('Started at: ' + str(datetime.datetime.utcnow()) + '  in seconds: ' + str(time.time()))

def send_one_message():
    pass

try:
    print("Messages will now be sent to device with %d second interval. Exit program with Ctrl-C." % MSG_INTERVAL_SEC)
    while True:
        # Acquire and format the time stamp
        timeStamp = datetime.datetime.utcnow()
        timeStamp_str = timeStamp.strftime('%Y-%m-%dT%H:%M:%S.%fZ')

        # Create the data string
        print("Creating a json data string...")
        data = str({"responseTimeoutInSeconds": 10, "payload": {"msg_id": "Shared-LiveDataResponse-1"}, "connectTimeoutInSeconds": 10, "methodName": "hub_direct_invoke_callback"})
        # data = {"responseTimeoutInSeconds": 10, "payload": {"msg_id": "Shared-LiveDataResponse-1"}, "connectTimeoutInSeconds": 10, "methodName": "hub_direct_invoke_callback"}


        # calculate time since sas was created
        currentTime = time.time()
        timeElapsed = currentTime - startTime

        # Create new sas if old one has expired
        if timeElapsed > sasTimeOut:
            device.create_sas(HUB_KEY,  'iothubowner', sasTimeOut)
            print(timeStamp_str + '; Created new SAS: ' + cloud._sas)
            startTime = currentTime

        # Send the data to Azure
        try:
            AzureSender = cloud.send(data)
        except Exception as e:
            print(timeStamp_str + '; Exception: %s' % e)
            exceptionCount += 1
            print('Success Count: ' + str(successCount) + '; Failure Count: ' + str(failureCount) + '; Exception Count: ' + str(exceptionCount))
            pass

        # Check for valid transmission
        if AzureSender == 204: # Successful Post
            print("Successfully sent message to hub.")
            successCount += 1

        elif AzureSender == 401: # Failed Authorization - Redo sas
            failureCount += 1
            print(timeStamp_str + '; Error Code: ' + str(AzureSender) + '; Create new sas')
            cloud.create_sas(sasTimeOut)
            print('New sas: ' + cloud._sas)
            print('Success Count: ' + str(successCount) + '; Failure Count: ' + str(failureCount) + '; Exception Count: ' + str(exceptionCount))

        else: # Failed transmission, record code
            failureCount += 1
            print(timeStamp_str + '; Error Code: ' + str(AzureSender))
            print('Success Count: ' + str(successCount) + '; Failure Count: ' + str(failureCount) + '; Exception Count: ' + str(exceptionCount))

        # print(timeStamp_str + '; Success Count: ' + str(successCount) + '; Failure Count: ' + str(failureCount))
        time.sleep(MSG_INTERVAL_SEC)
except KeyboardInterrupt:
    print("Interrupted by Ctrl-C. Exiting.")
