# Ansible Develop Guide

[TOC]


## 1. Ansible module
多数情况下，没有必要写自己的module，官方已经给我们提供了很多module，几乎涵盖了所有功能
[Ansible Modules](https://github.com/ansible/ansible/tree/devel/lib/ansible/modules)

当你有自己特殊的业务时，需要写自己的ansible module，如何写自己的ansible module呢 ？

***本课程将通过检测文件是否变化，写一个自己的模块***
_ _ _


## 2. Dynamic Inventory
当你所管理的机器比较少时，可以使用静态inventory来保存服务器和组的关系，但是当你的服务器越来越多的时候，你通常会考虑使用一个软件系统来存放inventory信息

提供inventory的软件系统有以下几种：
1. CMDB
2. 公有云提供商（AWS）
3. 企业内部私有云（openstack）

AWS和openstack,ansible已经提供了如何生成动态inventory的脚本，可以直接使用
[AWS ansible Dynamic inventory scripts](http://docs.ansible.com/ansible/latest/intro_dynamic_inventory.html#id6)
[Openstack ansible Dynamic inventory scripts](http://docs.ansible.com/ansible/latest/intro_dynamic_inventory.html#example-openstack-external-inventory-script)

***本课程通过建立一个简单的CMDB，并且使用python脚本从CMDB获取Dynamic Inventory***


_ _ _

## 3. Ansible Python API 
1. 什么是Ansible Python API ?
Ansible Python API是一组用python编写的类和函数，便于使用python程序调用Ansible的核心功能

2. 为什么要使用Ansible Python API ？
Ansible python API的应用场景主要有一下几种
    1. 前一次的执行结果作为后一次任务的参数输入
    2. 对任务的执行结果进行定制化输出或者存储
    3. 方便其他程序调用ansible的核心功能

3. 如何使用Ansible Python API ？

***本课程通过Ansible Python API 调用之前写的自定义模块来说明Ansible Python API如何使用***

_ _ _

## 4. Ansible Plugins
1. plugin是什么? 
回顾一下ansible的执行流程
[Ansible plugins](https://github.com/ansible/ansible/tree/devel/lib/ansible/plugins)
inventory --->由ansible.inventory模块创建，用于导入inventory文件 
variable_manage ---> 由ansible.vars模块创建，用于存储各类变量信息 
dataloader --->由ansible.parsing模块创建，用于数据解析 
options --->存放各类配置信息的nametuple 
passwords ---> 设置密码信息，例如become_pass 
callback ---> 回调函数,用于对返回结果进行处理 

2. 有哪些plugin?

action_plugins    
cache_plugins     
callback_plugins  
connection_plugins
lookup_plugins    
inventory_plugins 
vars_plugins      
filter_plugins    
test_plugins      
terminal_plugins  
strategy_plugins  

3. 如何使用plugin?

ansible.cfg中打开相关的plugin的配置

4. 如何扩展的plugin?

***本课程我们扩展一下callback plugin，并使用ansible运行看callback***




