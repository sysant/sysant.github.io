---
layout: post
title: ansible通过inventory动态分组 
categories: [ansible]
description: 基于/etc/hosts文件，通过inventory配置，ansible动态分组管理服务器
keywords: ansible hosts inventory
mermaid: false
sequence: false
flow: false
mathjax: false
mindmap: false
mindmap2: false
---

ansible通过inventory动态分组

## 1、说明

ansible既支持独立手动配置host文件来分组管理；也可以通过inventory结合python脚本通过指定hosts文件来动态分组；

以下我们通过线上某项目inventory自动将/etc/hosts中的服务器解析文件，动态生成对应项目组；好处是在/etc/hosts中一个地方配置解析就可以满足ansible和shell管理主机；

## 2、/etc/hosts文件

```shell
cat /etc/hosts
127.0.0.1 localhost.localdomain localhost
127.0.0.1 localhost4.localdomain4 localhost4

## OBT Server
10.186.186.2    hk-xgame-obt-center01
10.186.186.4    hk-xgame-obt-center02

10.186.186.10   hk-xgame-obt-fight01
10.186.186.7    hk-xgame-obt-fight02

10.186.186.36   hk-xgame-obt-zkongfun
10.186.186.22   hk-xgame-obt-zkongid   zkonggift
10.186.186.44   hk-xgame-obt-zkongplay zkongpush

10.186.186.24   hk-xgame-obt-pingbi01
10.186.186.45   hk-xgame-obt-pingbi02

10.186.186.87   hk-xgame-obt-game01
10.186.186.94   hk-xgame-obt-game02
10.186.186.123  hk-xgame-obt-game03

# pre
10.186.186.38  hk-xgame-pre-game01
10.186.188.7   hk-xgame-pre-zkong01   hk-xgame-cqc-game01

# test
10.186.188.7   hk-xgame-test01
```

## 3、ansible.cfg配置

```shell
egrep -v '^$|^#' ansible.cfg

[defaults]
inventory      = /etc/ansible/dynamic_hosts.py
forks          = 50
gathering = explicit
host_key_checking = False
deprecation_warnings = False
log_path = /var/log/ansible.log
command_warnings = False
[inventory]
[privilege_escalation]
[paramiko_connection]
[ssh_connection]
ssh_args = -C -o ControlMaster=auto -o ControlPersist=3d
control_path_dir = ~/.ansible/cp
control_path = %(directory)s/%%h-%%r
pipelining = True
[persistent_connection]
[accelerate]
[selinux]
[colors]
[diff]
```

## 4、dynamic_hosts.py自动分组

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 基于python的动态inventory脚本实例
# 2022-05-12 by san

import argparse
import re

try:
    import json
except ImportError:
    import simplejson as json

class DynamicInventory(object):
    def __init__(self):
        self.inventory = {}
        self.read_cli_args()
        #根据选项参数返回json
        if self.args.list:
            self.inventory = self.ret_inventory()
        elif self.args.host:
            self.inventory  = self.ret_inventory()
        else:
            self.inventory = self.empty_inventory()
        print json.dumps(self.inventory)

    def read_cli_args(self):
        # 定义选项参数
        parser = argparse.ArgumentParser()
        parser.add_argument('--list',dest='list',action = 'store_true')
        parser.add_argument('--host',dest='host',action = 'store')
        self.args = parser.parse_args()

    def ret_inventory(self):
        SUM = []
        host_group = ['pre','obt','pre-game','pre-zkong','obt-game','obt-center','obt-zkong','obt-fight','obt-pingbi']
        hostdict = {}
        for group in host_group:
            #re_string = "hk-sanguo-%s\w+" % group
            re_string = "hk-sanguo-%s\S+" % group
            with open('/etc/hosts', 'r') as f:
                li = re.findall(re_string, f.read())
                # remove special mathine
                #if 'cn-sd2-cb2p-gm' in li:
                #    li.remove('cn-sd2-cb2p-gm')
            hostdict[group] = {'hosts': li}
        return hostdict

    def empty_inventory(self):
        return {'_meta':{'hostvars':{}}}

if __name__ == '__main__':
    DynamicInventory()
    #h = DynamicInventory()
    #print h.ret_inventory()
```

## 5、测试

```shell
 ./dynamic_hosts.py --list
{"pre": {"hosts": ["hk-xgame-pre-game01", "hk-xgame-pre-zkong01"]}, "obt-center": {"hosts": ["hk-xgame-obt-center01", "hk-xgame-obt-center02"]}, "obt-game": {"hosts": ["hk-xgame-obt-game01", "hk-xgame-obt-game02", "hk-xgame-obt-game03"]}, "pre-game": {"hosts": ["hk-xgame-pre-game01"]}, "obt-fight": {"hosts": ["hk-xgame-obt-fight01", "hk-xgame-obt-fight02"]}, "pre-zkong": {"hosts": ["hk-xgame-pre-zkong01"]}, "obt": {"hosts": ["hk-xgame-obt-center01", "hk-xgame-obt-center02", "hk-xgame-obt-fight01", "hk-xgame-obt-fight02", "hk-xgame-obt-zkongfun", "hk-xgame-obt-zkongid", "hk-xgame-obt-zkongplay", "hk-xgame-obt-pingbi01", "hk-xgame-obt-pingbi02", "hk-xgame-obt-game01", "hk-xgame-obt-game02", "hk-xgame-obt-game03"]}, "obt-pingbi": {"hosts": ["hk-xgame-obt-pingbi01", "hk-xgame-obt-pingbi02"]}, "obt-zkong": {"hosts": ["hk-xgame-obt-zkongfun", "hk-xgame-obt-zkongid", "hk-xgame-obt-zkongplay"]}}

ansible pre -m ping
/usr/lib/python2.7/site-packages/ansible/parsing/vault/__init__.py:44: CryptographyDeprecationWarning: Python 2 is no longer supported by the Python core team. Support for it is now deprecated in cryptography, and will be removed in the next release.
  from cryptography.exceptions import InvalidSignature
[WARNING]: Invalid characters were found in group names but not replaced, use -vvvv to see details
hk-xgame-pre-game01 | SUCCESS => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python"
    }, 
    "changed": false, 
    "ping": "pong"
}
hk-xgame-pre-zkong01 | SUCCESS => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python"
    }, 
    "changed": false, 
    "ping": "pong"
}
```

