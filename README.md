# Ansible Develop Guide

## 环境准备

准备4台虚拟主机

IP|作用|主机名
---|---| ---
10.40.0.10 | ansible主机 |  cmdb01
10.40.0.11 | 被管理主机 | webserver01
10.40.0.12 | 被管理主机 | webserver02
10.40.0.13 | 被管理主机 | dbserver01

安装所需要的软件

在ansible主机10.40.0.10上安装所需要的软件


## 1. Dynamic Inventory

当你所管理的机器比较少时，可以使用静态inventory来保存服务器和组的关系，但是当你的服务器越来越多的时候，你通常会考虑使用一个软件系统来存放inventory信息

提供inventory的软件系统有以下几种：
1. CMDB
2. 公有云提供商（AWS）
3. 企业内部私有云（openstack）

AWS和openstack,ansible已经提供了如何生成动态inventory的脚本，可以直接使用

[AWS ansible Dynamic inventory scripts](http://docs.ansible.com/ansible/latest/intro_dynamic_inventory.html#id6)

[Openstack ansible Dynamic inventory scripts](http://docs.ansible.com/ansible/latest/intro_dynamic_inventory.html#example-openstack-external-inventory-script)




***本课程通过建立一个简单的CMDB，并且使用python脚本从CMDB获取Dynamic Inventory***



## 2. Ansible module

多数情况下，没有必要写自己的module，官方已经给我们提供了很多module，几乎涵盖了所有功能

可以使用ansible-doc --list 列出所有模块的使用帮助 [Ansible Modules](https://github.com/ansible/ansible/tree/devel/lib/ansible/modules)

当你有自己特殊的业务时，需要写自己的ansible module，如何写自己的ansible module呢 ？

***本课程将通过检测文件是否变化，实现自定义ansible模块***
_ _ _


_ _ _

## 3. Ansible Python API 
1. 什么是Ansible Python API ?

   Ansible Python API是一组用python编写的类和函数，便于使用python程序调用Ansible的核心功能

2. 为什么要使用Ansible Python API ？
   Ansible python API的应用场景主要有一下几种
   
    1. 前一次的执行结果作为后一次任务的参数输入
    2. 对任务的执行结果进行定制化输出或者存储
    3. 方便其他程序调用ans	ible的核心功能

3. 如何使用Ansible Python API ？

	***本课程通过Ansible Python API 调用之前写的自定义模块来说明Ansible Python API如何使用***

_ _ _

## 4. Ansible Plugins
1. plugin是什么? 

    回顾一下ansible python API的使用，讲解在哪些地方可以插入plugin

2. 有哪些plugin?

    - action_plugins
    - cache_plugins
    - callback_plugins
    - connection_plugins
    - lookup_plugins
    - inventory_plugins
    - vars_plugins
    - filter_plugins
    - test_plugins
    - terminal_plugins
    - strategy_plugins
    
3. 如何扩展plugin?

	***本课程我们扩展一下callback plugin，并使用ansible运行看callback***


4. 如何使用扩展的plugin?

   ansible.cfg中打开相关的plugin的配置





