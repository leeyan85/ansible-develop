# Ansible Plugins
## 1. plugin是什么? 

回顾一下ansible python API的使用，讲解在哪些地方可以插入plugin

## 2. 有哪些plugin?
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

## 3. 如何扩展plugin?

***本课程我们扩展一下callback plugin，并使用ansible运行看扩展plugin的运行结果***

## 4. 如何使用扩展的plugin?    

ansible.cfg中打开相关的plugin的配置，执行一个ansible module来查看运行结果
