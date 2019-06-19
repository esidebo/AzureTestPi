device=MimeRacer
echo "Will now send http request POST to $device device according to example at https://docs.microsoft.com/en-gb/azure/iot-hub/iot-hub-devguide-direct-methods"
echo "If you get Unauthorized return you need to generate a new sas token via 'az iot hub generate-sas-token --hub-name iothub-kistamobweek' (launch docker image with azure CLI)"
echo ""
curl -X POST \
   https://iothub-kistamobweek.azure-devices.net/twins/$device/methods?api-version=2018-06-30 \
   -H 'Authorization: SharedAccessSignature sr=iothub-kistamobweek.azure-devices.net&sig=gZ0rrGcEz8eG%2BwO3lYIGsBI9udccaMRdF9pih1pIU00%3D&se=1560810158&skn=iothubowner' \
   -H 'Content-Type: application/json' \
   -d '{
     "methodName": "reboot",
     "responseTimeoutInSeconds": 200,
     "connectTimeoutInSeconds": 5,
     "payload": {
        "input1": "someInput",
        "input2": "anotherInput"
     }
   }'
echo ""
