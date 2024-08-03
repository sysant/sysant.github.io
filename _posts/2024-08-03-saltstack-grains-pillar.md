---
layout: post
title: saltstack的grains与pillar使用入门 
categories: [saltstack]
description: saltstack的grains使用与pillar的入门
keywords: saltstack,grains,pillar
mermaid: false
sequence: false
flow: false
mathjax: false
mindmap: false
mindmap2: false
---

saltstack的grains与pillar使用入门



一、grains与pillar简介  

        grains是minion启动时加载，在minion运行过程中不会发生变化，所以是**静态数据**。grains数据的定制可以在各minion端，也可以放在master端;grains中包含许多的信息，如：运行的内核版本，操作系统，网络接口地址，MAC地址，cpu，内存等等信息。
Pillar是Salt用来分发全局变量到所有或指定minion的一个定制接口，所以相对grains来说可以称为动态的数据，保存在master端。

由于涉及的配置文件采用yaml格式，如果对yaml语法不在熟悉请访问这里

[http://www.ruanyifeng.com/blog/2016/07/yaml.html?f\=tt](http://www.ruanyifeng.com/blog/2016/07/yaml.html?f=tt)

最好也了解下jinjia2的格式，如不熟悉请访问这里
<http://docs.jinkan.org/docs/jinja2/intro.html> 

saltstack的安装部署请看这里http://dyc2005.blog.51cto.com/270872/1967147


二、grains日常使用入门

1、获取minion的grains所有数据

登录后复制  
```
salt "minion_152" grains.items 

```
登录后复制  
类似如图：

![saltstack grains与pillar使用和订制_saltstack](/images/saltstack/salt01.png)

2、获取单项grains值

登录后复制  
```bash
# salt "minion_152" grains.item os 
```
如图：

![saltstack grains与pillar使用和订制_ grains_02](/images/saltstack/salt02.png)

3、获取grains中的所有项(键)

登录后复制  
```bash
# salt "minion_152" grains.ls     #以minion_152上的为例
```
![saltstack grains与pillar使用和订制_saltstack_03](/images/saltstack/salt03.png)

这样就可通过grains.item  项去获取具体对应的值啦

4、在minion上订制grains数据

订制grains数据有两种方法分别如下：

方法一:

     修改/etc/salt/minion配置文件去掉12行左右的注释

     default_include: minion.d/*.conf

在/etc/salt/minion.d目录下

创建一个test.conf 内容如下：

登录后复制  
```
grains:               
   Data:
      - test
   Project:
      - wgdbl_game
```
重启minion
登录后复制  
```
# salt "minion_152" grains.items

```
如图：

![saltstack grains与pillar使用和订制_ pillar_04](/images/saltstack/salt04.png)

方法二:

在master操作

登录后复制  
```
mkdir -pv /srv/salt/_grains
cd  /srv/salt/_grains
cat hello.py
```
登录后复制  
```
#!/usr/bin/python
def GrainsHello():    
    grains = {}
    grains["project"] = "myTestProject"
    grains["name"] = "san game"   
    return grains

```
在服务端写好脚本再同步刷新到指定minion

登录后复制  
```
# salt "minion_152" saltutil.sync_grains

```
如图:

![saltstack grains与pillar使用和订制_saltstack_05](/images/saltstack/salt05.png)

推送更新成功。

此时到minion\_152所在的机器

/var/cache/salt/minion/files/base/_grains/会发现在master端创建的hello.py grains脚本已经推送至此，如图：

![grains与pillar使用和订制_pillar_06](/images/saltstack/salt06.png)

并且在该minion下的

/var/cache/salt/minion/extmods/grains下有执行的标记生成了hello.pyc

![saltstack grains与pillar使用和订制_ grains_07](/images/saltstack/salt07.png)

第一种方法是grains中的纯静态指定minion下生成并且要重启minion生效，第二种方法可以统一放在胳端管理，再推送到各指定minions 动态生成管理。

三、pillar的使用

1、获取指定minion上pillar的数据
首先与grains不同的是要获取pillar需要在master的配置文件中打开
取消552行的注释如下：
pillar_opts: True
并重启salt\-master

登录后复制  
```
# salt  "minion_152" pillar.data

```
如图：
![saltstack grains与pillar使用和订制_ grains_08](/images/saltstack/salt08.png)

**注意：最好不要在线上使用 salt "\*" pillar.data   这会卡的哦 **

2、pillar数据定制

配置master的pillar的根目录

取消529 -532 的注释

登录后复制  
```
529 pillar_roots:
530   base:
531     - /srv/pillar

```
创建根目录

mkdir -pv /srv/pillar

重启salt-master

切换到/srv/pillar目录

创建pillar顶层入口文件（相当于目录）top.sls,注意必须要以sls后缀。

登录后复制  
```
cat top.sls
base:   "*":      
   - data   "minion_152":
   - minion152* 1.

```
创建 data.sls

cat data.sls

登录后复制  
```
project_name: san
subject:
   - zgws
   - wgdbl 

```

创建 minion152.sls

cat minion152.sls

登录后执行
```
Minion_152: info
HostName:
   - zgws_game01
IP:
   - 172.16.3.152
game:
   - zgws

```
向minion同步pillar数据

登录后执行
```
# salt "minion_152" saltutil.refresh_pillar

```
如图：

![saltstack grains与pillar使用和订制_saltstack_09](/images/saltstack/salt09.png)

登录后执行  
```
# salt "minion_152" pillar.data
或
# salt "minion_152" pillar.items

```
如图：

![saltstack grains与pillar使用和订制_ pillar_10](/images/saltstack/salt10.png)

![saltstack grains与pillar使用和订制_ grains_11](/images/saltstack/salt11.png)

由于只对minion_152进行推送更新pIllar 因此其他的minion不会收到更新。

3、pillar配置文件中增加jinjia2格式的判断

cat top.sls

登录后复制  
```
base:
   "*":
      - data
   "minion_152":
      - minion152
      - osinfo 
```

创建osinfo.sls
cat osinfo.sls

登录后执行  
```
OS_INFO:
    - {{ grains.os}}
    {% if grains["os"] == "CentOS"%}
    - Linux System
    {% endif %}

```
刷新pillar数据

登录后复制  
```
# salt "minion_152" saltutil.refresh_pillar

```
查看minion_152 pillar数据

如图：

![saltstack grains与pillar使用和订制_saltstack_12](/images/saltstack/salt12.png)

通过grains和pillar可以很方便的定制出特定的数据，pillar 配置是完全保存在master端的，而grains既可以保存在master端也可以单独至minion端，每次修改需要重启minion端。pillar偏向敏感数据的统一存放在master端且灵活修改。


