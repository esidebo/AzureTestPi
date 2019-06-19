"""
    A simple implementation of Azure IoT Hub REST APIs to
    upload data from a Raspberry Pi to the Azure IoT Hub.
"""
# !/home/pi
import sys
# import DeviceClient
import Cloud

# Set the up required variables for Azure Iot Hub
AzureDeviceName = "MimeRacer"
AzureDeviceKey = "Le+4jMDLInzRQ68bFel+uDaGAfVBKD0rz7qRBaVY/IM="
AzureHubName = "iothub-kistamobweek"
sasTimeOut = 86400 #24 hours

# Create the device object and get the initial sas
cloud = Cloud.Cloud(AzureHubName.lower(), AzureDeviceName, AzureDeviceKey)
cloud.print_sas()

import Device
dev = Device(AzureHubName.lower(), AzureDeviceName, AzureDeviceKey))
print(dev.create_sas2())
