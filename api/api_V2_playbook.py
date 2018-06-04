#!/bin/env python
# -*- coding:utf8 -*-

from collections import namedtuple
from ansible.parsing.dataloader import DataLoader
from ansible.vars import VariableManager
from ansible.inventory import Inventory
from ansible.plugins.callback import CallbackBase
from ansible.executor.playbook_executor import PlaybookExecutor
import json
import time

import redis

def set_redis_connection():
    redis_cli=redis.Redis(host='127.0.0.1',port=6379,db=0)
    return redis_cli

def display_result_info(result):
    print (json.dumps(dir(result._host),indent=4))
    print (json.dumps(dir(result._result),indent=4))
    print (json.dumps(dir(result._task),indent=4))

def write_task_info_to_redis(result):
    redis_cli=set_redis_connection()
    for host_results in result:
        for key in host_results.keys():        
            print (key,host_results[key]._result)
            redis_cli.rpush(key,host_results[key]._result)
            

    
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


def playbook_run(playbook_path,host_inventory):
    loader = DataLoader()
    variable_manager = VariableManager()
    inventory = Inventory(loader=loader, variable_manager=variable_manager,host_list=host_inventory)
    variable_manager.set_inventory(inventory)
    passwords = dict(become_pass='')
    Options = namedtuple('Options',
                         ['connection',
                          'forks', 
                          'remote_user',
                          'ack_pass', 
                          'sudo_user',
                          'sudo',
                          'ask_sudo_pass',
                          'verbosity',
                          'module_path', 
                          'become', 
                          'become_method', 
                          'become_user', 
                          'check',
                          'listhosts', 
                          'listtasks', 
                          'listtags',
                          'syntax',
                          ])
    options = Options(connection='smart', 
                           forks=100,
                           remote_user='root',
                           ack_pass=None,
                           sudo_user='root',
                           sudo='yes',
                           ask_sudo_pass=True,
                           verbosity=5,
                           module_path=None,  
                           become=True, 
                           become_method='sudo', 
                           become_user='root', 
                           check=None,
                           listhosts=None,
                           listtasks=None, 
                           listtags=None, 
                           syntax=None
                      )
    
    # 多个yaml文件则以列表形式
    playbook = PlaybookExecutor(playbooks=[playbook_path],inventory=inventory,
                  variable_manager=variable_manager,
                  loader=loader,options=options,passwords=passwords)
                  
    results_callback=CallbackModule()
    
    playbook._tqm._stdout_callback=results_callback 
    
    result = playbook.run()
    
    write_task_info_to_redis(results_callback.host_ok)
    
    #print results_callback.host_unreachable
            
   
if __name__=='__main__':
    playbook_run('./api_v2.yml',['172.18.0.2','172.18.0.5'])
