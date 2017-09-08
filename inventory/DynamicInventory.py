#!/usr/bin/python 
import os
import sys
import argparse

try:
    import json
except ImportError:
    import simplejson as json


class Inventory(object):
    def __init__(self):
        self.inventory={}
        self.ReadCli()
        if self.args.list:
            self.inventory=self.GetInventory()
        elif self.args.host:
            self.inventory=self.GetInventory()
        else:
            self.inventory=self.EmptyInventory()
        print json.dumps(self.inventory,indent=4)

    def GetInventory(self):
        return {
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
                
    
    def EmptyInventory(self):
        return{'_meta':{'hostvars':{}}}
        
    def ReadCli(self):
        parser=argparse.ArgumentParser()
        parser.add_argument('--list',action='store_true')
        parser.add_argument('--host',action='store')
        self.args=parser.parse_args()

        
Inventory()
