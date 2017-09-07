# Dynamic Inventory
## 1. 为什么要使用动态Inventory ？

多数情况下，server信息会存在一些软件系统中，这些软件系统大概包括

1. CMDB
2. AWS EC2
3. Openstack [使用vagrant搭建openstack环境](https://github.com/openstack-ansible/openstack-ansible)
4. zabbix 监控系统
5. cobbler 一键装机系统

这时就需要从这些软件系统中获取动态Inventory

_ _ _

## 2. 动态Inventory格式

动态Inventory需要满足一定的json格式才能被ansible的核心模块所识别，格式如下

    {
        "webserver": {
            "hosts": [
                "192.168.33.11"
            ], 
            "vars": {
                "ansible_become_user": "vagrant", 
                "ansible_become_pass": "vagrant"
            }
        }, 
        "dbserver": {
            "hosts": [
                "192.168.33.12"
            ], 
            "vars": {
                "ansible_become_user": "root", 
                "ansible_become_pass": "secret"
            }
        }，  
        "_meta": {
            "hostvars": {
                "192.168.33.11": {
                    "software": "jboss"
                }, 
                "192.168.33.12": {
                    "software": "mysql"
                }
            }
        },     
    }


_ _ _


## 3. 从数据库中获取动态Inventory

### 3.1 安装一些软件

1. sudo apt-get install python-pip
2. sudo apt-get install redis-server
3. sudo apt-get install python-redis
4. sudo apt-get install python-sqlalchemy
5. sudo apt-get install python-mysqldb
6. sudo pip install pymysql
_ _ _

### 3.2 初始化数据库

1. 建立一个数据库 

   create database ansible_trainning character set utf8;

2. 导入示例数据库
   
   mysql ansible_trainning < ansible_trainning.sql

3. 给数据库用户赋予权限
   
   grant all privileges on ansible_trainning.* to ansibleuser identified by 'ansible';

_ _ _
   
### 3.3 获取动态Inventory

   使用例子中的脚本去获取动态inventory

### 3.4 使用动态inventory



