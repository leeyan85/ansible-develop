#ansible develop

[TOC]
## 1. Ansible module
多数情况下，没有必要写自己的module，官方已经给我们提供了很多module，几乎涵盖了所有功能
[Ansible Modules](https://github.com/ansible/ansible/tree/devel/lib/ansible/modules)

当你有自己特殊的业务时，需要写自己的ansible module，如何写自己的ansible module呢 ？

*本课程将通过检测文件是否变化，写一个自己的模块*
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

*本课程通过建立一个简单的CMDB，并且使用python脚本从CMDB获取Dynamic Inventory*


_ _ _

## 3. Ansible API
回顾一下ansible的执行流程，在这些执行流程中都会有plugin
![ansible的执行流程](http://)

1. 什么是Ansible API ？

2. 如何使用API ？

_ _ _

## 4. Ansible Plugins
1. plugin是什么 ？


2. 有哪些plugin ？
[Ansible plugins](https://github.com/ansible/ansible/tree/devel/lib/ansible/plugins)

3. 如何使用plugin ？
ansible.cfg中打开相关的plugin的配置

4. 如何编写自己的plugin ？
我们扩展一下callback plugin，并使用ansible运行看callback，plugin是否生效




