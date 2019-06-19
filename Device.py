"""
    An adaptation of the work done by Stepan Bechynsky
    found at https://github.com/bechynsky/AzureIoTDeviceClientPY
"""
import hmac
import base64
import urllib.parse
import requests



class Device():
    """
        Device for Azure IoT Hub REST API
        https://msdn.microsoft.com/en-us/library/mt590785.aspx
    """
    _API_VERSION = 'api-version=2018-06-30' # from https://docs.microsoft.com/en-us/rest/api/iothub/
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
        Generate Shared Access Signature according to https://docs.microsoft.com/en-gb/azure/iot-hub/iot-hub-devguide-security
    """
    def create_sas2(self, key, policy_name, expiry=3600): # 3600 s = 1 hour
        from hashlib import sha256

        ttl = time.time() + expiry
        sign_key = "%s\n%d" % ((urllib.quote_plus(uri)), int(ttl))
        print sign_key
        signature = base64.b64encode(hmac.HMAC(b64decode(key), sign_key, sha256).digest())
        rawtoken = {
            'sr' :  uri,
            'sig': signature,
            'se' : str(int(ttl))
        }
        if policy_name is not None:
            rawtoken['skn'] = policy_name
        
        return 'SharedAccessSignature ' + urllib.urlencode(rawtoken)

    """
        Creates Shared Access Signature. Run before another functions
        timeout - expiration in seconds
    """
    def create_sas(self, timeout):
        urlToSign = urllib.parse.quote(self._url_to_sign, safe='')

        # current time + timeout (seconds)
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
        # print("sas={}".format(self._sas))
        r = requests.post(self._base_url, data = message, headers=headers)

        return r.status_code
