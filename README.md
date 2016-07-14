# AzureTestPi
This repository contains the files that will allow a raspberry pi to communicate with Azure IoT hub using REST APIs.
## Resources
- [Microsoft Azure - Device Messaging REST APIs](https://msdn.microsoft.com/en-us/library/azure/mt590785.aspx)
  - This is the official Azure IoT Hub REST API documentation
- [Microsoft Azure - Shared Access Signatures](https://azure.microsoft.com/en-us/documentation/articles/storage-dotnet-shared-access-signature-part-1/)
  - The occifial documentation on creating a Shared Access Signature (sas)
- [Building an Azure Iot Demo Device with Raspberry Pi](http://robwhitehouse.azurewebsites.net/building-an-azure-iot-demo-device-with-raspberry-pi/)
  - This article was my main source of information as it is a complete example of what I was trying to do
- [bechynsky/AzureIoTDeviceClientPY GitHub Repository](https://github.com/bechynsky/AzureIoTDeviceClientPY)
  - A library that has already created the necessary functions to generate an sas in Python.
  - I tried to use the `deviceclient.send` function, but it failed and I could never get it to work. Instead of fighting with it, I wrote my own `send` function using the requests Python library.
- [Secure Sensor Streaming over HTTPS to Azure IoT Hub](https://www.hackster.io/glovebox/secure-sensor-streaming-over-https-to-azure-iot-hub-dba05d)
  - Occasionaly use to cross-reference the two above resources
- [Azure IoT Hub from Raspberry Pi 3](http://iottopic.com/azure-iot-hub-raspberry-pi-3/)
  - This article gives good information on getting the Pi set up

## Notes
- When setting the sas timeout (expiration time), there appears to be a 5 minute grace period. i.e. If the timeout is set to 0 seconds, the sas will work for the next 5 minutes.
- It has been determined that there is no need to use json.dumps to encode the data string as json. The requests library will simply accept a json formated string
  - i.e. `data = {'TimeStamp' : timeStamp_str, 'CPUTemp' : temp}`
- It is not a problem to use a longer sas expiration time. A 24 hour sas has successfully been tested. Doing this can reduce the nubmer of connections needed to Azure, thus reducing data usage.

## Recorded Error Codes & Exceptions
The descriptions for the error codes has been taken from [Mozilla Developer Network](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status).
- 401: Unauthorized - Authentication is needed to get requested response
  - This error is received when the sas is not valid
- 503: Service Unavailable - The server is not ready to handle the request
  - The origin of this error is at the server. The timing can not be predicted. This error means that the request did not go through.
- Exception - ('Connection aborted.', gaierror(-2, 'Name or service not known'))
  - This exception seems to occur randomly during the transmission of the messge to Azure as part of the underlying library. Over a single 24 hour test, the exception occured 7 times.
  - The `device.send(message)` command should be housed in a `Try{} Except{}` to handle the exception
