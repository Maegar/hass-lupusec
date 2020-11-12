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

""" Device module

Contains specific lupusec devices to retrieve information
or triggering actions.
"""

class GenericDevice(object):
    """ Generic Device Class 
    
    Contains the following data:
    - area ID
    - zone ID
    - device type
    - batter status
    - condition status
    - tamper status 
    """

    def __init__(self, area, zone, name, device_type):
        self.area = area
        self.zone = zone
        self.name = name
        self.device_type = device_type

    def set_battery(self, is_ok, status=''):
        """ Set battery status values """
        self.battery_ok = is_ok
        self.battery_status = status

    def set_tamper(self, is_ok, status=''):
        """ Set tamper status values """
        self.tamper_ok = is_ok
        self.tamper_status = status

    def set_cond(self, is_ok, status=''):
        """ Set condition status values """
        self.cond_ok = is_ok
        self.cond_status = status
    
    def set_status(self, status=''):
        """ Set status """
        self.status = status

    def __str__(self):
        return "Area: %s, Zone: %s, Type: %s, Name: %s, Battery: %s, Tamper: %s, Cond: %s, Status: %s" % (self.area, self.zone, self.device_type, self.name, self.battery_status, self.tamper_status, self.cond_status, self.status)
