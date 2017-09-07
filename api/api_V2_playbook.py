#!/bin/env python
# -*- coding:utf8 -*-

from collections import namedtuple
from ansible.parsing.dataloader import DataLoader
from ansible.vars import VariableManager
from ansible.inventory import Inventory
from ansible.executor.playbook_executor import PlaybookExecutor

loader = DataLoader()
variable_manager = VariableManager()
inventory = Inventory(loader=loader, variable_manager=variable_manager,host_list='hosts')
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
playbook = PlaybookExecutor(playbooks=['api_V2.yml'],inventory=inventory,
              variable_manager=variable_manager,
              loader=loader,options=options,passwords=passwords)
result = playbook.run()
print result
