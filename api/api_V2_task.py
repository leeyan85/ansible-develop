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
        self.host_unreachable[result._host.get_name()] = result #result是一个ansible返回的python对象
        
    def v2_runner_on_ok(self, result,  *args, **kwargs):  
        self.host_ok[result._host.get_name()] = result  #result是一个ansible返回的python对象

    def v2_runner_on_failed(self, result,  *args, **kwargs):  
        self.host_failed[result._host.get_name()] = result #result是一个ansible返回的python对象
 


def Order_Run(hosts, module_name, module_args):
    variable_manager = VariableManager()
    loader = DataLoader()
    print "#"*10
    inventory = Inventory(loader=loader, variable_manager=variable_manager, host_list=hosts)#2.0.0.0版本不支持host_list为列表格式
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
                    remote_user='vagrant', 
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
                    become_user='root',
                    become_method='sudo',
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
        results_raw['success'][host] = result._result
        print json.dumps(dir(result._task),indent=4) #如何查看result对象有哪些属性和方法
        print json.dumps(dir(result),indent=4) #如何查看result对象有哪些属性和方法
        
    for host, result in callback.host_failed.items():
        results_raw['failed'][host] = result._result
        
    for host, result in callback.host_unreachable.items():
        results_raw['unreachable'][host]= result._result
        
    return results_raw

if __name__=='__main__':    
    a=Order_Run(['192.168.33.11'],'shell','whoami')
    print a
