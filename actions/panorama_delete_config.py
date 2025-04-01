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


class DeleteConfig(BaseAction):
    ACTION_NAME = "delete config"

    def execute(self, connector):
        connector.debug_print(f"starting {self.ACTION_NAME} action")
        action_result = connector.add_action_result(ActionResult(dict(self._param)))

        xpath = self._param["xpath"]

        try:
            resp = connector.util._rest_delete_config(xpath=xpath)
        except (RuntimeError, requests.exceptions.HTTPError) as e:
            return action_result.set_status(phantom.APP_ERROR,
                                            consts.PAN_ERROR_MESSAGE.format(self.ACTION_NAME, e))

        action_result.add_data({"response_xml": resp.text})
        return action_result.set_status(phantom.APP_SUCCESS, f"Successfully ran action: {self.ACTION_NAME}")
