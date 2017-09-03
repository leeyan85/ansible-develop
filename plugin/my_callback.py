# (c) 2016, Matt Martz <matt@sivel.net>
#
# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.

'''
DOCUMENTATION:
    callback: json
    short_description: Ansbile screen output asjson
    version_added: "2.2"
    description:
        - This callback converts all events into JSON output
    type: stdout
    plugin_api_version: "2.0"
'''
import os
import sys
import json
from ansible.plugins.callback import CallbackBase
import redis
def write_result_to_redis():
    pass

class CallbackModule(CallbackBase):
    def __init__(self, *args, **kwargs):  
        super(CallbackModule, self).__init__(*args, **kwargs)  
        self.host_ok = {}  
        self.host_unreachable = {}  
        self.host_failed = {}

    def v2_runner_on_unreachable(self, result):  
        self.host_unreachable[result._host.get_name()] = result
        print  json.dumps(result._host.get_name())

    def v2_runner_on_ok(self, result,  *args, **kwargs):  
        self.host_ok[result._host.get_name()] = result
        print  json.dumps(result._host.get_name())

    def v2_runner_on_failed(self, result,  *args, **kwargs):  
        self.host_failed[result._host.get_name()] = result
        print  json.dumps(result._host.get_name())


