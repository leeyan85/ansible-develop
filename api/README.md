# Ansible Python API

## 1. Ansible Python API ？ 

Ansible Python API是一组用python编写的类和函数，便于使用python程序调用Ansible的核心功能
_ _ _

## 2. 为什么要使用Ansible Python API ？ 
Ansible python API的应用场景主要有一下几种

1. 前一次的执行结果作为后一次任务的参数输入
2. 对任务的执行结果进行定制化输出或者存储（引入一下callback plugin）
3. 方便其他程序调用ansible的核心功能

_ _ _

## 3. 如何使用Ansible Python API ？ 

讲解ansible API的调用流程，实例演示如何调用之前的自定义module
![ansible API的调用流程](https://github.com/leeyan85/ansible-develop/blob/master/ansible%20process.PNG)

- inventory --->由ansible.inventory模块创建，用于导入inventory文件
- variable_manage ---> 由ansible.vars模块创建，用于存储各类变量信息
- dataloader --->由ansible.parsing模块创建，用于数据解析
- options --->存放各类配置信息的nametuple
- passwords ---> 设置密码信息，例如become_pass
- callback ---> 回调函数,用于对返回结果进行处理

