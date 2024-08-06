---
layout: post
title: saltstack安装部署与使用入门 
categories: [saltstack]
description: AlamLinux8 安装saltstack以及基本入门使用
keywords: alamlinux,saltstack 
mermaid: false
sequence: false
flow: false
mathjax: false
mindmap: false
mindmap2: false
---

saltstack安装部署与使用入门



一、saltstack简介

     SaltStack 一种基于 C/S 架构的服务器基础架构集中化管理平台，管理端称为 Master，客户端称为 Minion。SaltStack 具备配置管理、远程执行、监控等功能，一般可以理解为是简化版的 Puppet 和加强版的 Func。SaltStack 本身是基于 Python 语言开发实现，结合了轻量级的消息队列软件 ZeroMQ 与 Python 第三方模块（Pyzmq、PyCrypto、Pyjinjia2、python\-msgpack 和 PyYAML 等）构建.

本文不以最新版安装部署，以AlamLinux8  python3.6.8环境中 在epel源中稳定的版本进行yum安装 。如需要安装最新版本下载地址（readhat/CentOS系）[官方安装源](https://docs.saltproject.io/salt/install-guide/en/latest/topics/install-by-operating-system/centos.html#install-centos)，


采用两台安装搭建基本的环境。一台做master/minion  一台minion

两台防火墙要么关闭 要么加上允许本地网段白名单类似 ：\-A INPUT \-s 172\.16\.3\.0/24 \-j ACCEPT

关闭selinux.


二、安装

1，安装epel扩展源

```bash
# yum install epel-release -y
```


2、安装saltstack master

```bash
# wget https://repo.saltproject.io/salt/py3/redhat/8/x86_64/latest.repo  -O /etc/yum.repos.d/
# yum install salt-master salt-minion  salt-ssh salt-syndic salt-api -y
# systemctl enable salt-master && sudo systemctl start salt-master
# systemctl enable salt-minion && sudo systemctl start salt-minion
# systemctl enable salt-syndic && sudo systemctl start salt-syndic
# systemctl enable salt-api && sudo systemctl start salt-api
```

修改主配置文件/etc/salt/master 内容如下：

```bash
# cat master |egrep -v '(^$|^#)'
interface: 0.0.0.0                #侦听地址
file_roots:                       #文件根目录
  base:
    - /srv/salt
    
# cat minion |egrep -v '(^$|^#)'
default_include: minion.d/*.conf      
master: 127.0.0.1               #和master在同一台
id: minion_local                #标识

### 查看启动salt-master和minion服务
# systemctl start salt-master 
# systemctl start salt-minion 

### 查看salt版本
# salt --version
salt 3007.1 (Chlorine)
```



2、安装minion(非master上）

```bash
# wget https://repo.saltproject.io/salt/py3/redhat/8/x86_64/latest.repo  -O /etc/yum.repos.d/
# yum install salt-minion -y
```

修改配置文件cat /etc/salt/minion

```bash
# cat minion |egrep -v '(^$|^#)'
default_include: minion.d/*.conf      
master: 172.16.3.147              #和master在同一台
id: minion_local                  #标识

### 启动minion服务 
# systemctl start salt-minion
```

三、master上添加minion

如里在master配置文件中打开

auto\_accept: True

则所有的minon 将会自动被认证加入。自行考量。本次是手工添加

```bash
# salt-key -L
```

如图：Unaccepted Keys:中出现两个等待授权认证的minon

![saltstack001](/images/saltstack/001.png)

```bash
# salt-key -A   
```
输入y

接受所有minion认证

再次salt-key -L 查看已授权的minion会就看到

```bash
# salt "\*" test.ping   \#查看所有的活动在线的minion
```

如图：

![saltstack_02](/images/saltstack/002.png")


到此基本的saltstack  master minion 环境安装部署基本配置完成

四、saltstack常用操作

除了上面的添加minon和测试minion在线情况外，还有一些其他的模拟提供一些常用操作;

1、salt语法

salt [客户端id，即目标，支持正规表达式] [模块名，如state，cmd。其实都是salt的模块] [动作]

如： salt "\*" test.ping       这里的"\*"就是匹配的目标，表示 所有minion   test是模块 ping是动作

目标有以下常用的五种形式：

指定目标主要有五种方式

     a)、Global，即salt默认的匹配方式，能识别终端常用的通配符，如\*代表所有

            如，salt '\*' test.ping

     b)、List，列表，需\-L指定。

            如，salt \-L 'minion\_local,minion\_152' test.ping 其中minion\_local,minion\_152

            是完整的minion\_id

     c)、\-E 正则表达式匹配

            如，salt \-E 'pre\[1\-7]' test.ping 会匹配pre1，pre2\..pre7，并且匹配到左右minion\_id

            里面含有1\-7的，如pre\-11,pre7也会匹配到，如果只匹配1\-7可使用参照下面

            如，salt \-E ^pre\[1\-7]$ test.ping或者 salt pre\[1\-7] test.ping

     d)、\-C 混合模式，里面可以既有正则表达式也有列表等

            salt \-C "minion\_\* or test\_minion" test.ping 匹配所有minion开头，或者test\_minion id的

     e)、分组，需要\-N指定，其中组名就是上面/etc/salt/master.d/groups.conf文件里面配置的

            配置信息。如，salt \-N apache test.ping

  

2、常用模块

然后是模块，主要介绍state，cmd，cp模块

注：想了解某个模块的功能或者具体参数可以

salt \* sys.doc \[模块名，如cmd]

a）、cmd模块

       salt '\*' cmd.run "echo $HOSTNAME"      这里可以远程执行shell命令，执行结果会返回

![saltstack_03](/images/saltstack/003.png)

b)、文件上传与下载

        salt "minion_152"  cp.get\_file  salt://files/test.txt /tmp/test.txt

        将/srv/salt/files/test.txt  推送到minion\_152 /tmp/下也叫test.txt

![saltstack_04](/images/saltstack/004.png)

         到minion\_152 tmp目录下查看

![saltstack_05](/images/salt/005.png) 

       同理可以通过 cp.push从minion上下载文件

        需要修改master中的   file\_recv: True

       salt "minion\_152" cp.push  /etc/fstab       \#默认下到本地

                        /var/cache/salt/master/minions/minion\-id/files目录

![saltstack_06](/images/saltstack/006.png)

其他的模块主参考官方文档。这里不再多说。  
