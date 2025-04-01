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
from datetime import datetime
import re

import panorama_consts as consts
from actions import BaseAction
import xml.etree.ElementTree as ET

class GenerateNextEntryName(BaseAction):
    ACTION_NAME = "Generate Next Entry Name"
    def execute(self, connector):
        connector.debug_print(f"starting {self.ACTION_NAME} action")
        action_result = connector.add_action_result(ActionResult(dict(self._param)))

        xpath = self._param["entry_xpath"]
        entry_name_prefix = self._param["entry_name_prefix"]
        assert len(entry_name_prefix) > 0

        date = self._param.get("date")
        if not date:
            date = datetime.now().strftime('%Y%m%d')
            connector.save_progress(f"Defaulting to today's date: {date.__repr__()}")


        try:
            xml = connector.util._rest_get_config(xpath=xpath)
        except requests.exceptions.HTTPError as e:
            return action_result.set_status(phantom.APP_ERROR,
                                            consts.PAN_ERROR_MESSAGE.format(self.ACTION_NAME, e))
        try:
            root = ET.fromstring(xml)
        except ET.ParseError as e:
            return action_result.set_status(phantom.APP_ERROR, f"API did not return valid XML: {e}")

        entries = root.findall('./result/entry')
        if len(entries) == 0:
            connector.save_progress("WARNING: No top-level <entry> elements found.")

        prefix_including_date = f"{entry_name_prefix}_{date}"
        connector.save_progress(f"Filtering top-level <entry/> elements with name starting with: prefix={prefix_including_date.__repr__()}")
        filtered = []

        pattern = re.compile(rf"{prefix_including_date}_(\d+)")

        largest_count = 0
        for entry in entries:
            name = entry.get('name', '')
            if name.startswith(prefix_including_date):
                m = re.fullmatch(pattern=pattern, string=name)
                if m:
                    assert len(m.groups()) == 1
                    count = int(m.groups()[0])
                    largest_count = max(largest_count, count)
                    connector.save_progress(f"Found entry with name {name.__repr__()} that matched prefix={prefix_including_date.__repr__()}")
                    filtered.append(entry)
        connector.save_progress(f"largest_count={largest_count}")

        new_entry_name = f"{prefix_including_date}_{largest_count+1}"
        connector.save_progress(f"New entry name: {new_entry_name.__repr__()}")

        action_result.add_data({'entry_name' : new_entry_name})
        return action_result.set_status(phantom.APP_SUCCESS, f"Successfully ran action {self.ACTION_NAME}")
