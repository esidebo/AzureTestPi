curl -v POST \
   https://iothub-kistamobweek.azure-devices.net/twins/MimeRacer/methods?api-version=2018-06-30 \
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



  # https://iothub-kistamobweek.azure-devices.net/messages/devicebound?api-version=2018-06-30 \
  # -H 'Authorization: SharedAccessSignature sr=iothub-kistamobweek.azure-devices.net&sig=GolYZGNFa%2FJ4Vq16RnH0A2wm9ETtNZhgZw3golgV2uo%3D&se=1560526235&skn=iothubowner' \
  # -H 'Content-Type: application/json' \
  # -d '{
  #     "payload": {
  #       "hostName": "iothub-kistamobweek.azure-devices.net",
  #       "owner": "twinUpdate",
  #       "key": "Q258tmmhnXPSAyKpcO6WexM4DATgb8cnhz63WMtsa0M=",
  #       "deviceID": "MimeRacer",
  #       "body": "{\"test\": \"This is a test\"}",
  #       "properties": "{"To": "hejsan"}"
  #     }
  #   }'

# -H 'To: /devices/MimeRacer/messages/devicebound' \
  # -d '{
  #   "payload": {
  #     "hostName": "iothub-kistamobweek.azure-devices.net",
  #     "owner": "twinUpdate",
  #     "key": "Q258tmmhnXPSAyKpcO6WexM4DATgb8cnhz63WMtsa0M=",
  #     "deviceID": "MimeRacer",
  #     "body": "{\"test\": \"This is a test\"}",
  #     "properties": "[]"
  #   }
  # }'

  # curl -v POST \
  #   https://main.iothub.ext.azure.com/api/Service/SendMessage/ \
  #   -H 'Authorization: SharedAccessSignature sr=iothub-kistamobweek.azure-devices.net&sig=0H9FrygE9kRK0IcYilaXDUhhT7Lirmzrux1w9l3gs90%3D&se=1560523374&skn=iothubowner' \
  #   -d '{
  #     "payload": {
  #       "hostName": "iothub-kistamobweek.azure-devices.net",
  #       "owner": "twinUpdate",
  #       "key": "Q258tmmhnXPSAyKpcO6WexM4DATgb8cnhz63WMtsa0M=",
  #       "deviceID": "MimeRacer",
  #       "body": "{\"test\": \"This is a test\"}",
  #       "properties": "[]"
  #     }
  #   }'

# '-H 'Authorization: SharedAccessSignature sr=iothub-kistamobweek.azure-devices.net%2F&sig=I0Ehcy6h8208RQhuOwlj7fQryvILbah2EWLTnP7TgNQ%3D&se=1560513727&skn=iothubowner' \
  # https://iothub-kistamobweek.azure-devices.net/twins/MimeRacer/methods?api-version=2018-06-30 \
  # -H 'Authorization: SharedAccessSignature sr=iothub-kistamobweek.azure-devices.net%2F&sig=I0Ehcy6h8208RQhuOwlj7fQryvILbah2EWLTnP7TgNQ%3D&se=1560513727&skn=iothubowner' \
  # -H 'Content-Type: application/json' \
  # -d '{
  #   "deviceId": "MimeRacer",
  #   "methodName": "reboot",
  #   "responseTimeoutInSeconds": 200,
  #   "payload": {
  #       "key": "value",
  #   }
  # }'
echo ""
