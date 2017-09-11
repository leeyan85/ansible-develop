#!/bin/env python
# -*- coding:utf8 -*-
import os
import sys
import json
import time
from ansible.plugins.callback import CallbackBase

def display_seperate(info):
    print info
    print '='*150
def display_result_info(result):
    print json.dumps(dir(result),indent=4)
    display_seperate('result._host')
    print json.dumps(dir(result._host),indent=4)
    display_seperate('result._result')
    print json.dumps(dir(result._result),indent=4)
    display_seperate('result._task')
    print json.dumps(dir(result._task),indent=4)

class CallbackModule(CallbackBase):
    def __init__(self, *args, **kwargs):  
        super(CallbackModule, self).__init__(*args, **kwargs)  
        self.host_ok = {}  
        self.host_unreachable = {}  
        self.host_failed = {}

    def v2_runner_on_unreachable(self, result):  
        self.host_unreachable[result._host.get_name()] = result
        display_result_info(result)

    def v2_runner_on_ok(self, result,  *args, **kwargs):  
        self.host_ok[result._host.get_name()] = result
        display_result_info(result)

    def v2_runner_on_failed(self, result,  *args, **kwargs):  
        self.host_failed[result._host.get_name()] = result
        display_result_info(result)

    def v2_playbook_on_play_start(self, play):
        self.playstarttime=time.time()
        
    def v2_playbook_on_task_start(self, task, is_conditional):
        self.taskstarttime=time.time()
