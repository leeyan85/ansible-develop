#!/usr/bin/python
#coding: utf-8
import os
import sys
import argparse
from models import Group,Host
from InitSqlSession import get_session

try:
    import json 
except ImportError:
    import simplejson as json
    
def get_inventory():
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
    #print json.dumps(inventory,indent=4)
    return inventory
    
def get_host_vars(host): 
    return inventory['_meta']['hostvars'][host]  

if __name__=='__main__':
    inventory = get_inventory()
    parser = argparse.ArgumentParser()
    parser.add_argument('--list',action='store_true',dest='list',help='get all hosts')
    parser.add_argument('--host',action='store',dest='host',help='get host vars')
    args=parser.parse_args()
    if args.list:
        inventory=get_inventory()
        print(json.dumps(inventory,indent=4))
    elif args.host:
        hostvar=get_host_vars(args.host)
        print(json.dumps({args.host:hostvar},indent=4))