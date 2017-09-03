#!/usr/bin/python
#coding: utf-8
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