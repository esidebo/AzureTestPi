curl -v -X POST \
  https://iothub-kistamobweek.azure-devices.net/devices/MimeRacer/messages/events?api-version=2018-06-30 \
  -H 'Authorization: SharedAccessSignature sr=iothub-kistamobweek.azure-devices.net%2Fdevices%2FMimeRacer&sig=TuwCGF1IlnmZP2rwvNGo7A%2Fo9gPJbtCo23R8dq8uui8%3D&se=1560597634' \
  -H 'Content-Type: application/json' \
  -d '{
    "payload": {
        "key": "value",
    }
  }'
