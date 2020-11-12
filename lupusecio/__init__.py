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

""" Lupusec XT1 / XT2 IO module

With this module a Lupusec alarm panel can be contacted. It is reversed engineered
from the web UI and can be used to receive information from such systems.

Typical usage example:
  system = LupusecSystem(lupusec_username, lupusec_password, lupusec_url)
  system.do_get_json('device_list_get')

"""

import requests
import json

class LupusecSystem(object):
    """ Lupusec system object to access the system """

    def __init__(self, username, password, url, verify_ssl=True):
        self._session = requests.Session()
        self._session.verify=verify_ssl
        self._alarm_panel_url = url
        self._session.auth = (username, password)
        self.sensors = []

    def do_get_json(self, endpoint):
        """ Perform a get request and read content as JSON """
        data = self._do_get(endpoint)
        return json.loads(data)

    def _do_get(self, endpoint):
        """ Perform a get request for specific endpoint and return the result

        e.g. http://192.168.1.44/action/specific-endpoint
        """
        response = self._session.get(self._alarm_panel_url + '/action/' + endpoint, timeout=15)
        return self._clean_json(response.text)

    def do_post_json(self, endpoint, formdata):
        """ Perform a post request for a specifc endpoint with the given
        content

        Interprete response as JSON
        """
        data = self._do_post(endpoint, formdata)
        return json.loads(data)

    def _do_post(self, endpoint, formdata):
        """ Perform a post request for a specifc endpoint with the given
        content
        """
        response = self._session.post(self._alarm_panel_url + '/action/' + endpoint, data=formdata, timeout=4)
        print(response.request.body)
        return self._clean_json(response.text)

    def _clean_json(self, textdata):
        """ Clean the body from not complaint data """
        textdata = textdata.replace("\t", "")
        if textdata.startswith("/*-secure-"):
            textdata = textdata[10:-2]

        return textdata
