device=MimeRacer
echo "Will now send http request POST to $device device according to example at https://docs.microsoft.com/en-gb/azure/iot-hub/iot-hub-devguide-direct-methods"
echo "If you get Unauthorized return you need to generate a new sas token via 'az iot hub generate-sas-token --hub-name iothub-kistamobweek' (launch docker image with azure CLI)"
echo ""
curl -v POST \
   https://iothub-kistamobweek.azure-devices.net/twins/$device/methods?api-version=2018-06-30 \
   -H 'Authorization: SharedAccessSignature sr=iothub-kistamobweek.azure-devices.net&sig=h4iK7v0kec0I4P%2B4s91%2FqYO0zW1Z6Q%2FEi1%2FF0dJv8do%3D&se=1560531143&skn=iothubowner' \
   -H 'Content-Type: application/json' \
   -d '{
     "methodName": "reboot",
     "responseTimeoutInSeconds": 200,
     "payload": {
        "input1": "someInput",
        "input2": "anotherInput"
     }
   }'
echo ""
