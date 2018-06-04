#!/usr/bin/python
#-*- coding:utf-8 -*-
import ansible.runner
import ansible.inventory
import ansible.playbook
from ansible import callbacks
from ansible import utils
import json
import sys

class VM(object):
    def __init__(self, ipAddress, userName, remoteUser):
        self.ipAddress = [ ipAddress ]
        self.userName = userName
        self.remoteUser = remoteUser

        '''init base info'''
        self.webInventory = ansible.inventory.Inventory(self.ipAddress)
        self.remotePort = 22
        self.timeOut = 10
        self.priKeyFile = '/home/%s/.ssh/id_rsa'%userName

    def RunTask(self):
        Runner = ansible.runner.Runner(
            module_name='command',
            module_args='uptime',
            inventory = self.webInventory
        )
        self.Output = Runner.run()

    def printoutput(self):
        print (json.dumps(self.Output,indent=4))
        print (self.priKeyFile)

    def RunPlaybook(self,playbook,hostlist): #playbook,用来指定playbook的yaml文件, hostlist 指定hosts文件
        stats = callbacks.AggregateStats() #收集playbook执行期间的状态信息，最后会进行汇总
        playbook_cb = callbacks.PlaybookCallbacks(verbose=utils.VERBOSITY) #callbacks用来输出playbook执行的结果
        runner_cb = callbacks.PlaybookRunnerCallbacks(stats,verbose=utils.VERBOSITY) #用来输出playbook执行期间的结果
        
        playbook=ansible.playbook.PlayBook(
            playbook=playbook,
            stats=stats,
            callbacks=playbook_cb,
            runner_callbacks=runner_cb,
            inventory = self.webInventory,
        )
        result=playbook.run()
        data = json.dumps(result,indent=4)
        return data
        
if __name__=='__main__':
    ip=sys.argv[1]
    vm = VM(ip, 'letv', 'asdfas')
    vm.RunPlaybook('/letv/scripts/ansible/restartvnc/restartvnc.yml','/letv/')
