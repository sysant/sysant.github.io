---
layout: post
title: 
categories: [51cto老博文]
description: 
keywords: 
mermaid: false
sequence: false
flow: false
mathjax: false
mindmap: false
mindmap2: false
---

把T-FLASH卡做成Ubuntu Linux开机登录钥匙和gufw防火墙配置


一、前言
----


作为IT从业者，个人笔记本电脑的安全由为重要，因为你的电脑上有连接公司各服务器的权限，和一些个人及公司隐私重要的资料，如果被别有用心的人非法使用，后果将不堪设想，出了纰漏这锅就背定了，因此个的笔记本电脑在没有授权情况下，是不能给其他人使用的;所谓防患未然嘛;  

本文主要从电脑网络层面与物理使用上加固;  
网络上，还是基于防火墙，ubuntu上有一个图形防火墙，底层也是基于iptables,就是gufw这个软件;规则是进出默认为拒绝，开放常用和日常使用的对外访问;对所在办公局域网信任，这样最大程度从网络上减少被攻～击可能性;  
小米pro 笔记本安装 ubuntu 16\.04  
![把T-FLASH卡做成Ubuntu开机登录钥匙和gufw防火墙配置](/images/把T-FLASH卡做成Ubuntu开机登录钥匙和gufw防火墙配置/把T-FLASH卡做成Ubuntu开机登录钥匙和gufw防火墙配置_gufw.png)  

如图：  
![把T-FLASH卡做成Ubuntu开机登录钥匙和gufw防火墙配置](/images/把T-FLASH卡做成Ubuntu开机登录钥匙和gufw防火墙配置/把T-FLASH卡做成Ubuntu开机登录钥匙和gufw防火墙配置_严格_02.png)  

物理上，由于现在主流笔记本基本上带T-FLASH插槽;我们就用登录密码加T-FLASH卡做开机的钥匙;开机密码这个一般都会设置的，关有密码，如果没有指定T-FLASH卡，是不允许登录的，效果如图：  
![把T-FLASH卡做成Ubuntu开机登录钥匙和gufw防火墙配置](/images/把T-FLASH卡做成Ubuntu开机登录钥匙和gufw防火墙配置/把T-FLASH卡做成Ubuntu开机登录钥匙和gufw防火墙配置_防火墙_03.png)  

一开机就是提示："system is going down"提示；点重试也没有用，一分钟后自动关机;此时如果插入了指定T\-FLASH则可以重试登录。

在机器运行中，如果插掉T-flash卡就会一分钟后悄悄关机，紧急时候可以直锁机接插卡走人;一分钟(可以自行修改)内插入卡则恢复;  

如图：（观察左上角有一个设备被拔了，再次插上时日志变化）  

![把T-FLASH卡做成Ubuntu开机登录钥匙和gufw防火墙配置_防火墙_04](/images/把T-FLASH卡做成Ubuntu开机登录钥匙和gufw防火墙配置/8fecda1888c241416f67ca12933b780f.gif)


如果插入了不是正确的TFLASH卡是没有用的，如图：（有一个闪存卡出现，但没有用，只有再次插上正确的T\-FLASH设备）  

![把T-FLASH卡做成Ubuntu Linux开机登录钥匙和gufw防火墙配置_通过_05](/images/把T-FLASH卡做成Ubuntu开机登录钥匙和gufw防火墙配置/76a46ee044290247158e83f2d38834d3.gif)  

如果你也是Ubuntu Linux办公;如果你也想做到这样，继续往下看：  

环境和工具：  

系统：ubuntu 16.04  

gufw 防火墙  

shell脚本  

T-FLASH卡一张  

准备好了吗？ go


思路
--


### 1、网络层面


安装gufw防火墙  

`sudo apt install gufw`  

按win图标 搜索gufw 如图：  

!\[把T-FLASH卡做成Ubuntu Linux开机登录钥匙和gufw防火墙配置](/images/把T-FLASH卡做成Ubuntu开机登录钥匙和gufw防火墙配置/把T-FLASH卡做成Ubuntu开机登录钥匙和gufw防火墙配置_严格_06\.png)


防火墙打开默认是关闭的（需要认证密码以root方式打开），先打开防火墙,此时默认传入规则为否认(拒绝外面访问本机即INPUT规则)，传出（允许，访问外面服务即OUTPUT规则）;  

传入 与传出 为否认即为DROP拒绝;此时只有开放了对应的规则才能被允许；接下来添加本地网络段172.16.0.0/16进出为信任;出去默认21 22 25 53 80 110 443 3389为信任;  

其他需要开放的请自行添加;以常用的添加信任网段和添加出去访问的端口为例


添加信任网段示例：  

![把T-FLASH卡做成Ubuntu开机登录钥匙和gufw防火墙配置](/images/把T-FLASH卡做成Ubuntu开机登录钥匙和gufw防火墙配置/把T-FLASH卡做成Ubuntu开机登录钥匙和gufw防火墙配置_严格_07.png)

添加访问80 web服务示例：  

![把T-FLASH卡做成Ubuntu开机登录钥匙和gufw防火墙配置](/images/把T-FLASH卡做成Ubuntu开机登录钥匙和gufw防火墙配置/把T-FLASH卡做成Ubuntu开机登录钥匙和gufw防火墙配置_严格_08.png)

开放本地的8000端口示例： 

![把T-FLASH卡做成Ubuntu开机登录钥匙和gufw防火墙配置](/images/把T-FLASH卡做成Ubuntu开机登录钥匙和gufw防火墙配置/把T-FLASH卡做成Ubuntu开机登录钥匙和gufw防火墙配置_防火墙_09.png)


好了，其他网段的信任添加和出去访问的端口类似;结合自己的实际需要添加！以上添加点高级部分可以记录日志！ 这里不演示了，毕竟这些都需要你息动手去尝试操作！  

网络层面就到这里完成！ 效果就是没有被开放不能进来，也不能出去！


### 物理层面


前面已经描述过了，个人笔记本的物理安全除了平时自己保管好外，笔记本电脑不在身边时，如果没有特定的T\-FLASH卡是不能正常开机登录系统的，即使登录了，紧急时，可以拔掉让笔记本自行关机，再次开机也是无法进入的，当然如果对Ubuntu Linxu熟悉的还是有办法，这里我就不提啦，防君子不防小人嘛，防小白不防大神哦！  

前的效果和描述已经看过了，直接上代码吧：  

需要rc.local服务是下正常运行并能开机运行的！  

![把T-FLASH卡做成Ubuntu开机登录钥匙和gufw防火墙配置](/images/把T-FLASH卡做成Ubuntu开机登录钥匙和gufw防火墙配置/把T-FLASH卡做成Ubuntu开机登录钥匙和gufw防火墙配置_防火墙_10.png)


登录后复制  
```
### 主要作用开机运行并检查 并运行开机守护进行(循环检查)
# cat /etc/rc.local
status=$(ls -l /dev/disk/by-uuid/ |grep mmcblk0p1 |awk '{print $9}')
Check(){
echo $status
if [ ${status} = "DA28BC3228BC0F8D" ];
then 
echo "Welcome dongyc login at $(date +%F-%H-%M-%S)" >>/home/dongyc/Login.txt
else
  echo "$(date +%F-%H-%M-%S) login failed!" >>/home/dongyc/Login.txt
  shutdown -h +1
fi
}
Check
nohup /home/dongyc/CHECK.sh >/tmp/check.out 2>&1  &
exit 0

## 以上DA28BC3228BC0F8D  我的T-flash设备的识别号，唯一

# cat /home/dongyc/CHECK.sh
#!/bin/sh
while true
do
  sleep 2
  ## 检测TFLASH卡是否挂载存在
  status=$(ls -l /dev/disk/by-uuid/ |grep mmcblk0p1 |awk '{print $9}')
  ## 判断是否存在,并检查变量stat是否为空(即是否触发了关机操作)

  ### TFLASH存在同时stat为空
  if [ "${status}" = "DA28BC3228BC0F8D" -a  -n ${stat} ]
   then
     echo "${status} is exsit.Login OK~" >> /tmp/check.log
     ### TFLASH存在和stat为空时保持取消关机,因为此时表明正常状态
     shutdown -c
     stat="" 
  else
     ## 如果stat有值同时TFLASH没有存在挂载;说明触发了关机操作，或者已经是reboot (两者一回事) 跳过检查执行关机
     if [ "${stat}" = "reboot" ]
        then
           continue
     else
     ## TFLASH不存在,执行关机,设置stat为reboot,并记录到日志中
        time=$(date +%F-%H-%M-%S)
        echo "At ${time} Can't found TFLASH,I think is not my master login.system reboot after 1 min." >>/tmp/check.log
        stat=$(shutdown  -h +1;echo "reboot")
     fi
  fi
done

```

至此，从网络和物理层面的控制，安全上基本上还看的过去了吧？其实做这个的初衷就是为了把笔记本电脑做成一个有FLASH为钥匙多功能可以扩充哦，比如如果没有T\-FLASH卡，除了关机外关机前可以把重要的资料删除！

