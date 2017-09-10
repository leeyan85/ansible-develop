#!/bin/env python
# -*- coding:utf8 -*-
from ansible.plugins.callback import CallbackBase
import json
import time
import logging
import redis

def set_redis_connection():
    redis_cli=redis.Redis(host='127.0.0.1',port=6379,db=0)
    return redis_cli

def display_result_info(result):
    print json.dumps(dir(result._host),indent=4)
    print json.dumps(dir(result._result),indent=4)
    print json.dumps(dir(result._task),indent=4)

def write_task_info_to_redis(result):
    redis_cli=set_redis_connection()
    for host_results in result:
        for key in host_results.keys():        
            print key,host_results[key]._result
            redis_cli.rpush(key,host_results[key]._result)
            
def write_task_info_to_log(info):    
    logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='myapp.log',
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
        #display_result_info(result)

    def v2_runner_on_ok(self, result, *args, **kwargs):  
        self.host_ok.append({result._host.get_name():result})
        #display_result_info(result)
        endtime=time.time()
        #print result._host.get_name(),result._task.name,self.playstarttime,self.taskstarttime,endtime   
        
    def v2_runner_on_failed(self, result,  *args, **kwargs):  
        self.host_failed[result._host.get_name()] = result
        #display_result_info(result)

    def v2_playbook_on_play_start(self, play):
        self.playstarttime=time.time()
        
    def v2_playbook_on_task_start(self, task, is_conditional):
        self.taskstarttime=time.time()


    def v2_playbook_on_play_start(self, play):
        self.playstarttime=time.time()
        
    def v2_playbook_on_task_start(self, task, is_conditional):
        self.taskstarttime=time.time()

if __name__=="__main__":
    write_result_to_redis()
    
    
