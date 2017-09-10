#!/bin/env python
# -*- coding:utf8 -*-
import os
import sys
import json
import time
from ansible.plugins.callback import CallbackBase
import redis
   
def set_redis_connection():
    redis_cli=redis.Redis(host='127.0.0.1',port=6379,db=0)
    return redis_cli


def write_task_info_to_redis(result):
    redis_cli=set_redis_connection()
    for key in result.keys():        
        print key,result[key]._result
        redis_cli.rpush(key,result[key]._task)    

            
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
        write_task_info_to_redis(self.host_ok)
    def v2_runner_on_failed(self, result,  *args, **kwargs):  
        self.host_failed[result._host.get_name()] = result
        display_result_info(result)

    def v2_playbook_on_play_start(self, play):
        self.playstarttime=time.time()
        
    def v2_playbook_on_task_start(self, task, is_conditional):
        self.taskstarttime=time.time()
