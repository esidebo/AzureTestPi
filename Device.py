import hmac
import base64
import urllib.parse
import requests
import time


class Device():
    """
        Device for Azure IoT Hub REST API
        https://msdn.microsoft.com/en-us/library/mt590785.aspx
    """
    _API_VERSION = 'api-version=2016-02-03'
    _HEADER_AUTHORIZATION = 'Authorization'

    """
        iot_hub_name - name of your Azure IoT Hub
        device_name - name of your device
        key - security key for your device
    """
    def __init__(self, iot_hub_name, device_name, key):
        self._iot_hub_name = iot_hub_name
        self._device_name = device_name
        self._key = key

        self._base_url = 'https://' + \
                        self._iot_hub_name + \
                        '.azure-devices.net/devices/' + \
                        self._device_name + \
                        '/messages/events?' + self._API_VERSION

        self._url_to_sign = self._iot_hub_name + \
                        '.azure-devices.net/devices/' + \
                        self._device_name

    """
        Creates Shared Access Signature. Run before another funstions
        timeout - expiration in seconds
    """
    def create_sas(self, timeout):
        urlToSign = urllib.parse.quote(self._url_to_sign, safe='') 
        
        # current time +10 minutes
        timestamp = int(time.time()) + timeout

        h = hmac.new(base64.b64decode(self._key), 
                    msg = "{0}\n{1}".format(urlToSign, timestamp).encode('utf-8'),
                    digestmod = 'sha256')

        self._sas = "SharedAccessSignature sr={0}&sig={1}&se={2}".format(urlToSign, 
                    urllib.parse.quote(base64.b64encode(h.digest()), safe = ''),
                    timestamp)

        return self._sas

    def send(self, message):
    	headers = {
    		self._HEADER_AUTHORIZATION : self._sas,
    		'Content-Type' : 'application/json'
    	}

    	r = requests.post(self._base_url, data = message, headers=headers)
    	
    	return r.status_code