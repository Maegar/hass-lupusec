#!/usr/bin/env python3
# Copyright 2020 Paul Proske
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

""" Alarm panel module

Can be used to retrieve information and trigger actions from alarm panel.
"""

import requests
import json

from homeassistant.components.hass_lupusec.lupusecio.devices.Generic import GenericDevice
import homeassistant.components.hass_lupusec.lupusecio.devices.Translation as TRANS

class AlarmPanel(object):
    """ Lupusec XT1+, XT2, XT2+, XT3 alarm panel """

    ACTION_HISTORY_GET = 'recordListGet'
    ACTION_SENSOR_LIST_GET = 'deviceListGet'
    ACTION_PANEL_CONDITION_GET = 'panelCondGet'
    MODE_TRANSLATION = {'4' : 'HOME3', '3' : 'HOME2', '2' : 'HOME', '0' : 'DISARM', '1' : 'ARM'}


    def __init__(self, lupusec_system):
        self._name = "XT Zentrale"
        self._lupusec_system = lupusec_system
        self._sensors = {}
        self._history = None
        self.areas = []
        self.areas.append(Area(self, 1))
        self.areas.append(Area(self, 2))
        #self.do_update()

    def do_update(self):
        """ do update for all """
        self.do_update_history()
        self.do_update_sensors()
        self.do_update_panel_cond()
        #doUpdateCameras()

    def do_update_mode(self, area):
        self._lupusec_system.do_post_json()

    def do_update_sensors(self):
        sensor_list = self._lupusec_system.do_get_json(self.ACTION_SENSOR_LIST_GET)['senrows']
        for device in sensor_list:

            device_type = TRANS.XT2_TRANSLATIONS[device['type_f']]
            device_name = device['name']
            device_area_id = device['area']
            device_zone_id = device['zone']
            device_status = '' if device['status'] == '' else TRANS.XT2_TRANSLATIONS[device['status']]

            device_tamper_ok = int(device['tamper_ok'])
            device_tamper_status = '' if device_tamper_ok else TRANS.XT2_TRANSLATIONS[device['tamper']]

            device_battery_ok = int(device['battery_ok'])
            device_battery_status = '' if device_battery_ok else TRANS.XT2_TRANSLATIONS[device['battery']]

            device_cond_ok = int(device['cond_ok'])
            device_cond_status = '' if device_cond_ok else TRANS.XT2_TRANSLATIONS[device['cond']]

            _id = '%s-%s' % (device_area_id, device_zone_id)
            _device = self._sensors.get(_id)
            if not _device:
                _device = GenericDevice(device_area_id, device_zone_id, device_name, device_type)
                self._sensors[_id] = _device

            _device.set_battery(device_battery_ok, device_battery_status)
            _device.set_tamper(device_tamper_ok, device_tamper_status)
            _device.set_cond(device_cond_ok, device_cond_status)
            _device.set_status(device_status)

    def do_update_panel_cond(self):
        self._panel_conditions = self._lupusec_system.do_get_json(self.ACTION_PANEL_CONDITION_GET)
        for area in self.areas:
            area.update_conditions(self._panel_conditions)
        self._battery = self._evaluate_panel_condition(self._panel_conditions, 'battery_ok', {'1': True, '0': False})
        self._tamper = self._evaluate_panel_condition(self._panel_conditions, 'tamper_ok', {'1': True, '0': False})

    def _evaluate_panel_condition(self, panel_conditions, field, enum):
        if panel_conditions['updates'][field] not in enum:
            return 'UNKNOWN'
        else:
            return enum[panel_conditions['updates'][field]]

    def do_update_history(self):
        self._history = []
        for entry in self._lupusec_system.do_get_json(self.ACTION_HISTORY_GET)['logrows']:
            indexEventEnd = entry['event'].index('}')
            eventName = entry['event'][0:indexEventEnd+1]
            event = TRANS.XT2_TRANSLATIONS[eventName]
            if '%s' in event:
                event = event % (entry['area'])
            self._history.append({'date': entry['time'], 'time': entry['time'], 'Sensor': entry['name'], 'Type': TRANS.XT2_TRANSLATIONS[entry['type_f']], 'Event': event})

    def __str__(self):
        return "Lupusec: %s, mode_area1: %s, mode_area2: %s" % (self._name, self.area1.get_mode(), self.area2.get_mode())


class Area(object):

    ACTION_PANEL_CONDITION_ENDPOINT_POST = 'panelCondPost'

    def __init__(self, alarmPanel, areaNo = None):
        self.alarmPanel = alarmPanel
        self.areaNo = areaNo

    def update_conditions(self, panelConditions):
        if panelConditions['updates']['alarm_ex'] == "1" or not 'Normal':
            self._mode = 'TRIGGERED'
        else:
            fieldValue = 'pcondform' + (str(self.areaNo) if self.areaNo is not None else "")
            self._mode = self.alarmPanel.MODE_TRANSLATION[panelConditions['forms'][fieldValue]['mode']]

    def set_mode(self, modeToSwitch):
        """ Set the new mode corresponding to the given value
        If requests fails false will be returned otherwise true
        """
        flippedValues = dict([(value, key) for key, value in self.alarmPanel.MODE_TRANSLATION.items()])
        dataToSend = {'mode':flippedValues[modeToSwitch]}
        if self.areaNo is not None:
            dataToSend['area'] = self.areaNo
        request = self.alarmPanel._lupusec_system.do_post_json(self.ACTION_PANEL_CONDITION_ENDPOINT_POST, dataToSend)

        return request['result'] == 1

    def get_mode(self):
        return self._mode

    def is_arm(self):
        return self._mode == 'ARM'

    def is_home(self):
        return self._mode == 'HOME'

    def is_night(self):
        return self._mode == 'HOME2'

    def is_custom_bypass(self):
        return self._mode == 'HOME3'

    def is_disarm(self):
        return self._mode == 'DISARM'

    def is_triggered(self):
        return self._mode == 'TRIGGERED'

    def set_arm(self):
        self.set_mode('ARM')

    def set_disarm(self):
        self.set_mode('DISARM')

    def set_home(self):
        self.set_mode('HOME')

    def set_night(self):
        self.set_mode('HOME2')

    def set_custom_bypass(self):
        self.set_mode('HOME3')