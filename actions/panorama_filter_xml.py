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
import json
import xml.etree.ElementTree as ET

import phantom.app as phantom
from phantom.action_result import ActionResult

from actions import BaseAction


class FilterXML(BaseAction):
    def execute(self, connector):
        connector.debug_print(f"starting filter xml action with params={self._param}")
        action_result = connector.add_action_result(ActionResult(dict(self._param)))

        xml = self._param["xml"]
        xpath_filter = self._param.get("xpath")
        attribute_filter = self._param.get("attribute_filter")
        attribute_filter_dict = {}
        if attribute_filter:
            try:
                attribute_filter_dict = json.loads(attribute_filter)
            except json.decoder.JSONDecodeError as e:
                return action_result.set_status(phantom.APP_ERROR,
                                                f"Invalid JSON for attribute_filter={attribute_filter}. ERROR: {e}")

        try:
            root = ET.fromstring(xml)
        except ET.ParseError as e:
            return action_result.set_status(phantom.APP_ERROR, f"XML is not valid: {e}")
        nodes = root.findall(xpath_filter)

        results = []
        for node in nodes:
            for attribute_name, attribute_value_contains in attribute_filter_dict.items():
                if attribute_value_contains not in node.attrib.get(attribute_name, ""):
                    break
            else:
                results.append(ET.tostring(node))

        for result in results:
            action_result.add_data({'xml': result})
        return action_result.set_status(phantom.APP_SUCCESS, "Successfully fetched config")
