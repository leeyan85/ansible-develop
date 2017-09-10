#!/bin/env python
# -*- coding:utf8 -*-
from ansible.plugins.callback import CallbackBase
import json
import time
import logging

def display_result_info(result):
    print json.dumps(dir(result._host),indent=4)
    print json.dumps(dir(result._result),indent=4)
    print json.dumps(dir(result._task),indent=4)
           
def write_task_info_to_log(info):    
    logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='/data/ansible_run.log',
                    filemode='w')
        
    logging.debug(info)
    logging.info(info)
    logging.warning(info)

    
class CallbackModule(CallbackBase): #callback plugin
    def __init__(self, *args, **kwargs):  
        super(CallbackModule, self).__init__(*args, **kwargs)  
        self.host_ok = []
        self.host_unreachable = {}  
        self.host_failed = {}
        self.task_ok={}
        self.playstarttime='play start time'
        self.taskstarttime='task start time'

    def v2_runner_on_unreachable(self, result):
        self.host_unreachable[result._host.get_name()] = result

    def v2_runner_on_ok(self, result, *args, **kwargs):  
        self.host_ok.append({result._host.get_name():result})
        endtime=time.time()
        print endtime
        info="%s %s %s %s %s"%(result._host.get_name(),result._task.name,self.playstarttime,self.taskstarttime,endtime)
        print info
        write_task_info_to_log(info)
        
    def v2_runner_on_failed(self, result,  *args, **kwargs):  
        self.host_failed[result._host.get_name()] = result

    def v2_playbook_on_play_start(self, play):
        self.playstarttime=time.time()
        
    def v2_playbook_on_task_start(self, task, is_conditional):
        self.taskstarttime=time.time()


    def v2_playbook_on_play_start(self, play):
        self.playstarttime=time.time()
        
    def v2_playbook_on_task_start(self, task, is_conditional):
        self.taskstarttime=time.time()

