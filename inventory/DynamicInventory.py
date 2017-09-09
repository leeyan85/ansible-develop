#!/usr/bin/python 
import os
import sys
import argparse

try:
    import json
except ImportError:
    import simplejson as json

example_inventory={
                'servers': {
                            'vars':{
                                    'package':'servers_var',
                            },
                            'children': ['webservers','dbservers'],
                },
                'webservers':{
                            'hosts':['172.18.0.2'],
                            'vars':{
                                    'package':'group_web_var',
                                    'ansible_become_pass':'password',
                                    'ansible_become_user':'root',
                                    'ansible_become': True,
                                    'ansible_become_method':'su',                                      

                             }
                 },
                 'dbservers':{
                            'hosts':['172.18.0.5'],
                            'vars':{
                                    'package':'group_db_var',
                             }
                 },
                 '_meta' : {
                        'hostvars':{
                            '172.18.0.2':{
                                        'package':'host_web_var',
                                      
                            },
                            '172.18.0.5':{
                                'package': 'host_db_var',
                            },
                        }
                  }

            }   

            
class Inventory(object):
    def __init__(self):
        self.inventory=example_inventory
        self.read_cli()
        if self.args.list:
            self.inventory=self.get_inventroy()
        elif self.args.host:
            print self.args.host
            self.inventory=self.get_host_vars(self.args.host)
        else:
            self.inventory=self.empty_inventory()
        print json.dumps(self.inventory,indent=4)

    def get_inventroy(self):
        return self.inventory
    
    def empty_inventory(self):
        return{'_meta':{'hostvars':{}}}
        
    def get_host_vars(self,host):
        return self.inventory['_meta']['hostvars'][host]
        
    def read_cli(self):
        parser=argparse.ArgumentParser()
        parser.add_argument('--list',action='store_true',dest='list',help='get all hosts')
        parser.add_argument('--host',action='store',dest='host',help='get host vars')
        self.args=parser.parse_args()

        
Inventory()
