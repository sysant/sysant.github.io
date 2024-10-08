---
layout: post
title: saltstack基于pillar统一配置iptables防火墙实战
categories: [saltstack]
description: saltstack基于pillar统一配置iptables防火墙实战
keywords: saltstack,pillar,iptables
mermaid: false
sequence: false
flow: false
mathjax: false
mindmap: false
mindmap2: false
---

saltstack基于pillar统一配置iptables防火墙实战

## 一、概述

grains是minion启动时加载，在minion运行过程中不会发生变化，所以是静态数据。grains数据的定制可以在各minion端，也可以放在master端;grains中包含许多的信息，如：运行的内核版本，操作系统，网络接口地址，MAC地址，cpu，内存等等信息。  

Pillar主要用来保存各minion自定义变量;是Salt用来分发变量到所有或指定minion的一个定制接口，所以相对grains来说可以称为动态的数据，保存在master端。  

本文将基于pillar为各主机定制要开放的白名单ip和要开放的对外服务，以及自身要出去访问的服务;因为线上防火墙默认规则是drop的，因此需要定义以上三种规则，以上三种规则将在pillar和salt配置中体现。

本文测试环境可以是redhat系统 CentOS6 或7，基于iptables saltstack版本2016\.10上测试 通过;我想逻辑应该是一样的;  

saltstack redhat系上[yum源地址](https://repo.saltstack.com/yum/redhat/)  

salt安装配置这里忽略可查看之前文章

### 二、配置主机pillar

1. 针对10.8.11.171配置防火墙规则,pillar定义规则

```
# cat /srv/pillar/top.sls
base:
  10.8.11.171:
  - webname.web10-8-11-125
  - hosts.hosts10_8_11_125
  - iptables.open.web
  - iptables.access.ntp
  - iptables.access.web
  - iptables.access.sms
  - iptables.whiteip.offices


# cat /srv/pillar/iptables/whiteip/offices.sls
white_ips:
   allow_offices1:
      allowip: 10.8.0.0/16

   allow_offices2:
      allowip: 61.188.188.188
			
###对外开放web服务配置，其他配置类似			
# cat /srv/pillar/iptables/open/web.sls
open_allow:
  http_open_allow:
    port: 80
    procto: 'tcp'

### 访问外面的服务，其他访问服务类似
#cat  /srv/pillar/iptables/access/ntp.sls
out_allow:
  ntp_out_allow:
    port: 123
    procto: 'udp'
```

说明：下次10\.8\.11\.171主机要开放服务时就修改/srv/pillar/top.sls文件挂载要开放的服务（\- iptables.open.xxx）这个xxx要在/srv/pillar/iptables/open/目录下xxx.sls 格式如前页的web.sls;添加出去访问服务时（\- iptables.access.yyy）这个yyy要在/srv/pillar/iptables/access/yyy.sls格式如前面的ntp.sls;当要添加白名单ip服务时（\- iptables.whiteip.zzz）这个zzz.sls 要在/srv/pillar/iptables/whiteip/zzz.sls 格式类似offices.sls


2. salt state配置

```bash
cat /srv/salt/top.sls
base:
  10.8.11.171:
  - base.env_init
  - iptables.init
  - nginx.env_init
  - php.env_init

……以下省略……

```

由于 包含的配置较多，可以从[这里](https://github.com/sysant/studys/blob/main/scripts/top.sls)下载

说明：在推送iptables规则前清除已有的规则;再从pillar的配置文件循环读取并配置防火规则;最后设置iptables默认策略INPUT OUTPUT FORWARD 为DROP; 有人可能就要问了，为舍搞这么复杂，防火开起来开放一些规则就行了，为啥非得把默认策略设置DROP，进出都得要规则？如果这么问请[看下这里](http://blog.51cto.com/dyc2005/2106138)～

### 三、规则推送

1. 查看主机的pillar


```
#  salt 10.8.11.171 pillar.data

```

如图：可以看出以上的配置白名单ip与开放和访问服务端口  

![saltstack_pillar_iptables01](/images/saltstack/pillar01.png)  

![saltstack_pillar_iptables02](/images/saltstack/pillar02.png)


2. 推送到主机


```
# salt 10.8.11.171 state.sls iptables.init

最后出现类似下面的表示已经推送配置成功
Summary for 10.8.11.171
-------------
Succeeded: 43 (changed=42)
Failed:     0
-------------
Total states run:     43
Total run time:    3.120 s


### 查看iptables 配置
# iptables -vnL
```

如图：  

![saltstack_pillar_iptables03](/images/saltstack/pillar03.png)  

开放的白名单和开放的服务以及能出去访问的服务已经都有了;另外默认策略已经是DROP；这样只有开放的白名单和允许出去访问服务才能出去，很好的阻止了反弹式木\-马主动出去访问的情况，同时只允许开放的服务才能进来;其他情况一律拒绝;不过需要注意的是，在生产线上改造时，勿必确认好主机开放的服务和需要出去访问或调用其他主机的服务端口，否则会误伤，你懂滴！为什么非得搞这么严格这么麻烦，这样安全啊，防止反弹式木\-马效果好呀～！  
至些salt 通过pillar 配置防火墙规则完成！下次再写个基于zabbix的监控，监控被droped的包，再报警，这样可以及时发现防火墙状态和问题～敬请期待吧～

本文基于生产线salt配置，是整理备忘，如有不妥之处欢迎指正与交流 ！谢谢～

