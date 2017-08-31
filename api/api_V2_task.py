
#!/bin/env python
# -*- coding:utf8 -*-
import os
import sys
import json
from collections import namedtuple
from ansible.parsing.dataloader import DataLoader
from ansible.vars import VariableManager
from ansible.inventory import Inventory
from ansible.playbook.play import Play
from ansible import constants as C
from ansible.plugins.callback import CallbackBase
from ansible.executor.task_queue_manager import TaskQueueManager


class ResultCallback(CallbackBase):
    def __init__(self, *args, **kwargs):  
        super(ResultCallback, self).__init__(*args, **kwargs)  
        self.host_ok = {}  
        self.host_unreachable = {}  
        self.host_failed = {}  

    def v2_runner_on_unreachable(self, result):  
        self.host_unreachable[result._host.get_name()] = result  

    def v2_runner_on_ok(self, result,  *args, **kwargs):  
        self.host_ok[result._host.get_name()] = result  

    def v2_runner_on_failed(self, result,  *args, **kwargs):  
        self.host_failed[result._host.get_name()] = result



def Order_Run(hosts, module_name, module_args):
    variable_manager = VariableManager()
    loader = DataLoader()
    print "#"*10
    inventory = Inventory(loader=loader, variable_manager=variable_manager, host_list='hosts')
    print '#'*10
    Options = namedtuple('Options',
                        ['listtags', 
                        'listtasks',
                        'listhosts', 
                        'syntax', 
                        'connection',
                        'module_path', 
                        'forks',
                        'remote_user',
                        'private_key_file', 
                        'ssh_common_args',
                        'ssh_extra_args',
                        'sftp_extra_args', 
                        'scp_extra_args', 
                        'become', 
                        'become_method', 
                        'become_user', 
                        'verbosity', 
                        'check'])
    options = Options(
                    listtags=False, 
                    listtasks=False,
                    listhosts=False, 
                    syntax=False, 
                    connection='ssh', 
                    module_path=None, 
                    forks=100, 
                    remote_user='letv', 
                    private_key_file=None, 
                    ssh_common_args=None, 
                    ssh_extra_args=None, 
                    sftp_extra_args=None, 
                    scp_extra_args=None, 
                    become=True, 
                    become_method='sudo', 
                    become_user='root', 
                    verbosity=None, 
                    check=False)
    
    passwords = dict(become_pass=None)
    play_source = dict(
                    name="test ansible tasks",
                    hosts='all',
                    gather_facts='no',
                    become=True,
                    become_user='andbase',
                    become_method='su',
                    tasks=[
                        dict(action=dict(module=module_name, args=module_args)),
                        dict(action=dict(module='command', args='id'))
                    ]
                    )
    print json.dumps(play_source,indent=4)
    play = Play().load(play_source, variable_manager=variable_manager, loader=loader)
    tqm = None
    callback = ResultCallback()
    try:
        tqm = TaskQueueManager(
                inventory=inventory,
                variable_manager=variable_manager,
                loader=loader,
                options=options,
                passwords=passwords,
                stdout_callback=callback,
                run_additional_callbacks=C.DEFAULT_LOAD_CALLBACK_PLUGINS,
                run_tree=False,
                )
        
        result = tqm.run(play)
        print result
    finally:
        if tqm is not None:
            tqm.cleanup()
            
    results_raw = {}
    results_raw['success'] = {}
    results_raw['failed'] = {}
    results_raw['unreachable'] = {}

    for host, result in callback.host_ok.items(): 
        results_raw['success'][host] = json.dumps(result._result)
  
    for host, result in callback.host_failed.items():
        results_raw['failed'][host] = result._result['msg']  
  
    for host, result in callback.host_unreachable.items():
        results_raw['unreachable'][host]= result._result['msg']  
    
    return results_raw
    

hosts={
        'servers': {
                    'vars':{
                            'package':'servers_var',
                    },
                    'children': ['webservers','dbservers'],
        },
        'webservers':{
                    'hosts':['10.75.30.29'],
                    'vars':{
                            'package':'group_web_var',
                     }
         },
         'dbservers':{
                    'hosts':['10.75.30.29'],
                    'vars':{
                            'package':'group_db_var',
                     }
         },
         
         '_meta' : {
                'hostvars':{
                    '10.75.30.29':{
                        'become_pass':'123456',
                    },
                }
          }
    }
        
a=Order_Run('hosts','shell','whoami')
print a