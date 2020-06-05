from http.client import HTTPSConnection
from base64 import b64encode, b64decode
import xt1_const as XT1_CONST
import xt2_const as XT2_CONST
import const as GENERAL
import demjson
import json
import ssl

class LupusecSystem(object):

    def __init__(self, username, password, url):
        self.headers = {
            "Authorization": "Basic {}".format(b64encode(bytes(f"{username}:{password}", "utf-8")).decode("ascii")),
            "content-type": "application/x-www-form-urlencoded"
        }
        self.client = HTTPSConnection(url, context = ssl._create_unverified_context())
        self.sensors = []

    def getDeviceList(self):
        pass

    def getAlarmPanelStatus(self):
        pass
    
    def doGet(self, url):
        self.client.request('GET', '/action' + url, headers=self.headers)
        res = self.client.getresponse()
        charset = 'utf-8'
        #print(res.getheader("Content-Type").split("=")[1]) #TODO replace with requestes module
        return str(res.read(), charset)

class XT2(LupusecSystem):
    def __init__(self, username, password, url):
        super().__init__(username, password, url)

    def getDeviceList(self):
        sensorList = self.doGet('/deviceListGet')['senrows']
        for device in sensorList:    
            deviceName = device['name']
            deviceId = device['zone']
            deviceTamper = False if int(device['tamper_ok']) else True

            if device['type'] not in XT2_CONST.TYPES:
                deviceType = 'UNKNOWN'
            else:
                deviceType = XT2_CONST.TYPES[device['type']]

            if deviceType in GENERAL.BINARY_SENSOR_TYPES:
                status = XT2_CONST.STATUS[device['status']]
                lupuDev = LupusecBinaryDevice(status, deviceId, deviceName, deviceType, deviceTamper)
            else:
                lupuDev = LupusecDevice(deviceId, deviceName, deviceType, deviceTamper)

            self.sensors.append(lupuDev)  
        return self.sensors

    def getAlarmPanelStatus(self):
        return self.doGet('/panelCondGet')
    
    def doGet(self, url):
        jsData = super().doGet(url)
        print(repr(jsData))
        return json.loads(jsData)

class XT1(LupusecSystem):

    def __init__(self, username, password, url):
        super().__init__(username, password, url)

    def getDeviceList(self):
        sensorList = self.doGet('/sensorListGet')['senrows']
        for device in sensorList:
            
            deviceName = device['name']
            deviceId = device['no']

            if device['type'] not in XT1_CONST.TYPES:
                deviceType = 'UNKNOWN'
            else:
                deviceType = XT1_CONST.TYPES[device['type']]

            if deviceType in GENERAL.BINARY_SENSOR_TYPES:
                status = XT1_CONST.STATUS[device['cond']]
                lupuDev = LupusecBinaryDevice(status, deviceId, deviceName, deviceType)
            else:
                lupuDev = LupusecDevice(deviceId, deviceName, deviceType)

            self.sensors.append(lupuDev)  
        return self.sensors

    def getAlarmPanelStatus(self):
        return self.doGet('/panelCondGet')
    
    def doGet(self, url):
        jsData = self.__clean_json(super().doGet(url))
        return demjson.decode(jsData)

    def __clean_json(self, textdata):
            textdata = textdata.replace("\t", "")
            i = textdata.index('\n')
            textdata = textdata[i+1:-2]
            return textdata

class LupusecDevice(object):

    def __init__(self, deviceId, name, devType, tamper = False):
        self.deviceId = deviceId
        self.name = name
        self.type = devType
        self.tamper = tamper

    def __str__(self):
        return "ID: %s, Device: %s, Name: %s, Tamper: %d" % (self.deviceId, self.type, self.name, self.tamper)

class LupusecBinaryDevice(LupusecDevice):

    def __init__(self, status, deviceId, name, devType, tamper = False):
        super().__init__(deviceId, name, devType, tamper)
        self.status = status

    def __str__(self):
        return "%s, Status: %s" % (super().__str__(), self.status)

    def is_on_open(self):
        return self.status == GENERAL.Status.OPEN | self.status == GENERAL.Status.ON

    def is_off_closed(self):
        return self.status == GENERAL.Status.CLOSED | self.status == GENERAL.Status.OFF

user = ""
password = ""
url_or_ip = ""

system = XT2(user, password, url_or_ip)

for device in system.getDeviceList():
    print(device)
