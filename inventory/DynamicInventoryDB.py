#!/usr/bin/env python
import os
import sys
import argparse
from models import Group,Host
from InitSqlSession import get_session

try:
    import json
except ImportError:
    import simplejson as json


class Inventory(object):
    def __init__(self):
        self.inventory={}
        self.read_cli_args()
        if self.args.list:
            self.inventory=self.example_inventory()
        elif self.args.host:
            self.inventory=self.empty_inventory()
        else:
            self.inventory=self.empty_inventory()
        print json.dumps(self.inventory,indent=4)
        
    def empty_inventory(self):
        return{'_meta':{'hostvars':{}}}
        
    def read_cli_args(self):
        parser=argparse.ArgumentParser()
        parser.add_argument('--list',action="store_true")
        parser.add_argument('--host',action='store')
        self.args=parser.parse_args()
        
    def example_inventory(self):
        session=get_session()
        #groups=session.query(Group).filter(Group.name==u'dbserver').all()
        groups=session.query(Group).all()
        inventory={}
        inventory={'_meta':{'hostvars':{}}}
        for group in groups:
            hosts=[host.IP for host in group.host_list]
            vars={  
                    'ansible_become_user':group.username,
                    'ansible_become_pass':group.password,
                }
            inventory[group.name]={
                    'hosts':hosts,
                    'vars':vars,
            }
            for host in group.host_list:
                inventory['_meta']['hostvars'][host.IP]={
                        'software':host.software
                }
        #print json.dumps(inventory,indent=4)
        return inventory
    


def example_inventory():
    session=get_session()
    #groups=session.query(Group).filter(Group.name=='webserver').all()
    groups=session.query(Group).all()
    inventory={'_meta':{'hostvars':{}}}
    for group in groups:
        hosts=[host.IP for host in group.host_list]
        vars={ 
                'ansible_become':True,
                'ansible_become_method':'su',
                'ansible_become_user':group.username,
                'ansible_become_pass':group.password,
            }
        inventory[group.name]={
                'hosts':hosts,
                'vars':vars,
        }
        for host in group.host_list:
            inventory['_meta']['hostvars'][host.IP]={
                        'software':host.software,
            }
    print json.dumps(inventory,indent=4)
    #return json.dumps(inventory,indent=4)

#example_inventory()

Inventory()
