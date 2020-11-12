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

import sys
import re

class ContactId:
    Pattern = re.compile(r'^\[(.+) 18(.)(.{3})(.{2})(.{3})(.{4})\]')

    def __init__(self, data):
        """ Initialize the Contact ID object """
        self.raw = data
        match = ContactId.Pattern.match(str(data, encoding='utf-8'))

        if match:
            self.subscriber = match.group(1).strip()
            self.qualifier = QUALIFIER[match.group(2)]
            self.event = match.group(3)
            self.eventtext = EVENTS[match.group(3)]
            self.group = match.group(4)
            self.sensor = match.group(5)
            self.checksum = match.group(6)
            self.valid = self._calculate_fletcher_checksum(data, 16) == (match[6])

    def _calculate_fletcher_checksum(self, data, len):
        sum1 = 0
        sum2 = 0
        i = 1
        while (len):
            tlen = 256 if (len > 256) else len
            len -= tlen

            while (tlen != 0):
                sum1 += data[i]
                sum1 = (sum1 & 0xFF)
                sum2 += sum1
                sum2 = (sum2 & 0xFF)
                tlen -= 1
                i += 1
        return hex(sum2 << 8 | sum1).replace('0x','').upper()
    
    def __str__(self):
        return "Subscriber: %s, Qualifier: %s, Event: %s, EventText: %s, Group: %s, Sensor: %s, ChecksumOk: %s" % (self.subscriber, self.qualifier, self.event, self.eventtext, self.group, self.sensor, self.valid)

QUALIFIER = {
    '1': r'New Event / opening',
    '3': r'New Restore / closing',
    '6': r'Previously reported condition still present (Status report)'
}

EVENTS = {
    '100': r'Medical',
    '101': r'Personal Emergency',
    '102': r'Fail to report in',
    '110': r'Fire',
    '111': r'Smoke',
    '112': r'Combustion',
    '113': r'Water flow',
    '114': r'Heat',
    '115': r'Pull Station',
    '116': r'Duct',
    '117': r'Flame',
    '118': r'Near Alarm',
    '120': r'Panic',
    '121': r'Duress',
    '122': r'Silent',
    '123': r'Audible',
    '124': r'Duress – Access granted',
    '125': r'Duress – Egress granted',
    '130': r'Burglary',
    '131': r'Perimeter',
    '132': r'Interior',
    '133': r'24 Hour (Safe)',
    '134': r'Entry/Exit',
    '135': r'Day/night',
    '136': r'Outdoor',
    '137': r'Tamper',
    '138': r'Near alarm',
    '139': r'Intrusion Verifier',
    '140': r'General Alarm',
    '141': r'Polling loop open',
    '142': r'Polling loop short',
    '143': r'Expansion module failure',
    '144': r'Sensor tamper',
    '145': r'Expansion module tamper',
    '146': r'Silent Burglary',
    '147': r'Sensor Supervision Failure',
    '150': r'24 Hour Non-Burglary',
    '151': r'Gas detected',
    '152': r'Refrigeration',
    '153': r'Loss of heat',
    '154': r'Water Leakage',
    '155': r'Foil Break',
    '156': r'Day Trouble',
    '157': r'Low bottled gas level',
    '158': r'High temp',
    '159': r'Low temp',
    '161': r'Loss of air flow',
    '162': r'Carbon Monoxide detected',
    '163': r'Tank level',
    '200': r'Fire Supervisory',
    '201': r'Low water pressure',
    '202': r'Low CO2',
    '203': r'Gate valve sensor',
    '204': r'Low water level',
    '205': r'Pump activated',
    '206': r'Pump failure',
    '300': r'System Trouble',
    '301': r'AC Loss',
    '302': r'Low system battery',
    '303': r'RAM Checksum bad',
    '304': r'ROM checksum bad',
    '305': r'System reset',
    '306': r'Panel programming changed',
    '307': r'Self- test failure',
    '308': r'System shutdown',
    '309': r'Battery test failure',
    '310': r'Ground fault',
    '311': r'Battery Missing/Dead',
    '312': r'Power Supply Overcurrent',
    '313': r'Engineer Reset',
    '320': r'Sounder/Relay',
    '321': r'Bell 1',
    '322': r'Bell 2',
    '323': r'Alarm relay',
    '324': r'Trouble relay',
    '325': r'Reversing relay',
    '326': r'Notification Appliance Ckt. # 3',
    '327': r'Notification Appliance Ckt. #4',
    '330': r'System Peripheral trouble',
    '331': r'Polling loop open',
    '332': r'Polling loop short',
    '333': r'Expansion module failure',
    '334': r'Repeater failure',
    '335': r'Local printer out of paper',
    '336': r'Local printer failure',
    '337': r'Exp. Module DC Loss',
    '338': r'Exp. Module Low Batt.',
    '339': r'Exp. Module Reset',
    '341': r'Exp. Module Tamper',
    '342': r'Exp. Module AC Loss',
    '343': r'Exp. Module self-test fail',
    '344': r'RF Receiver Jam Detect',
    '350': r'Communication trouble',
    '351': r'Telco 1 fault',
    '352': r'Telco 2 fault',
    '353': r'Long Range Radio xmitter fault',
    '354': r'Failure to communicate event',
    '355': r'Loss of Radio supervision',
    '356': r'Loss of central polling',
    '357': r'Long Range Radio VSWR problem',
    '370': r'Protection loop',
    '371': r'Protection loop open',
    '372': r'Protection loop short',
    '373': r'Fire trouble',
    '374': r'Exit error alarm (zone)',
    '375': r'Panic zone trouble',
    '376': r'Hold-up zone trouble',
    '377': r'Swinger Trouble',
    '378': r'Cross-zone Trouble',
    '380': r'Sensor trouble',
    '381': r'Loss of supervision - RF',
    '382': r'Loss of supervision - RPM',
    '383': r'Sensor tamper',
    '384': r'RF low battery',
    '385': r'Smoke detector Hi sensitivity',
    '386': r'Smoke detector Low sensitivity',
    '387': r'Intrusion detector Hi sensitivity',
    '388': r'Intrusion detector Low sensitivity',
    '389': r'Sensor self-test failure',
    '391': r'Sensor Watch trouble',
    '392': r'Drift Compensation Error',
    '393': r'Maintenance Alert',
    '400': r'Open/Close',
    '401': r'O/C by user',
    '402': r'Group O/C',
    '403': r'Automatic O/C',
    '404': r'Late to O/C (Note: use 453, 454 instead )',
    '405': r'Deferred O/C (Obsolete- do not use )',
    '406': r'Cancel',
    '407': r'Remote arm / disarm',
    '408': r'Quick arm',
    '409': r'Keyswitch O/C',
    '441': r'Armed STAY',
    '442': r'Keyswitch Armed STAY',
    '450': r'Exception O/C',
    '451': r'Early O/C',
    '452': r'Late O/C',
    '453': r'Failed to Open',
    '454': r'Failed to Close',
    '455': r'Auto-arm Failed',
    '456': r'Partial Arm',
    '457': r'Exit Error (user)',
    '458': r'User on Premises',
    '459': r'Recent Close',
    '461': r'Wrong Code Entry',
    '462': r'Legal Code Entry',
    '463': r'Re-arm after Alarm',
    '464': r'Auto-arm Time Extended',
    '465': r'Panic Alarm Reset',
    '466': r'Service On/Off Premises',
    '411': r'Callback request made',
    '412': r'Successful download/access',
    '413': r'Unsuccessful access',
    '414': r'System shutdown command received',
    '415': r'Dialer shutdown command received',
    '416': r'Successful Upload',
    '421': r'Access denied',
    '422': r'Access report by user',
    '423': r'Forced Access',
    '424': r'Egress Denied',
    '425': r'Egress Granted',
    '426': r'Access Door propped open',
    '427': r'Access point Door Status Monitor trouble',
    '428': r'Access point Request To Exit trouble',
    '429': r'Access program mode entry',
    '430': r'Access program mode exit',
    '431': r'Access threat level change',
    '432': r'Access relay/trigger fail',
    '433': r'Access RTE shunt',
    '434': r'Access DSM shunt',
    '501': r'Access reader disable',
    '520': r'Sounder/Relay Disable',
    '521': r'Bell 1 disable',
    '522': r'Bell 2 disable',
    '523': r'Alarm relay disable',
    '524': r'Trouble relay disable',
    '525': r'Reversing relay disable',
    '526': r'Notification Appliance Ckt. # 3 disable',
    '527': r'Notification Appliance Ckt. # 4 disable',
    '531': r'Module Added',
    '532': r'Module Removed',
    '551': r'Dialer disabled',
    '552': r'Radio transmitter disabled',
    '553': r'Remote Upload/Download disabled',
    '570': r'Zone/Sensor bypass',
    '571': r'Fire bypass',
    '572': r'24 Hour zone bypass',
    '573': r'Burg. Bypass',
    '574': r'Group bypass',
    '575': r'Swinger bypass',
    '576': r'Access zone shunt',
    '577': r'Access point bypass',
    '601': r'Manual trigger test report',
    '602': r'Periodic test report',
    '603': r'Periodic RF transmission',
    '604': r'Fire test',
    '605': r'Status report to follow',
    '606': r'Listen- in to follow',
    '607': r'Walk test mode',
    '608': r'Periodic test - System Trouble Present',
    '609': r'Video Xmitter active',
    '611': r'Point tested OK',
    '612': r'Point not tested',
    '613': r'Intrusion Zone Walk Tested',
    '614': r'Fire Zone Walk Tested',
    '615': r'Panic Zone Walk Tested',
    '616': r'Service Request',
    '621': r'Event Log reset',
    '622': r'Event Log 50% full',
    '623': r'Event Log 90% full',
    '624': r'Event Log overflow',
    '625': r'Time/Date reset',
    '626': r'Time/Date inaccurate',
    '627': r'Program mode entry',
    '628': r'Program mode exit',
    '629': r'32 Hour Event log marker',
    '630': r'Schedule change',
    '631': r'Exception schedule change',
    '632': r'Access schedule change',
    '641': r'Senior Watch Trouble',
    '642': r'Latch-key Supervision',
    '651': r'Reserved for Ademco Use',
    '652': r'Reserved for Ademco Use',
    '653': r'Reserved for Ademco Use',
    '654': r'System Inactivity',
    '750': r'Motion detection',
    '751': r'Motion detection',
    '760': r'Home automation rule executed'
}