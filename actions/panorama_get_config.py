# File: panorama_get_address.py
#
# Copyright (c) 2016-2025 Splunk Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under
# the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
# either express or implied. See the License for the specific language governing permissions
# and limitations under the License.

import phantom.app as phantom
import requests
from phantom.action_result import ActionResult

import panorama_consts as consts
from actions import BaseAction
import xml.etree.ElementTree as ET

class GetConfig(BaseAction):
    def execute(self, connector):
        connector.debug_print("starting get config action")
        action_result = connector.add_action_result(ActionResult(dict(self._param)))

        xpath = self._param["xpath"]

        try:
            xml = connector.util._rest_get_config(xpath=xpath)
        except requests.exceptions.HTTPError as e:
            return action_result.set_status(phantom.APP_ERROR,
                                            consts.PAN_ERROR_MESSAGE.format("get config", e))
        try:
            ET.fromstring(xml)
        except ET.ParseError as e:
            return action_result.set_status(phantom.APP_ERROR, f"API did not return valid XML: {e}")
        action_result.add_data({'xml' : xml})
        return action_result.set_status(phantom.APP_SUCCESS, "Successfully fetched config")
