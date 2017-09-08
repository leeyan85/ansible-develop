#!/bin/env python
# -*- coding:utf8 -*-

import os
import sys
import json
from ansible.plugins.callback import CallbackBase
from InitRedis import set_redis_connection

def write_result_to_redis():
    redis_cli=set_redis_connection()
    redis_cli.set('name','lee')
    print redis_cli.get('name')


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

if __name__=="__main__":
    write_result_to_redis()
    
    
