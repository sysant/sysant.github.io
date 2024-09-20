---
layout: post
title: saltapi安装配置实践
categories: [saltstack]
description: AlamLinux8 基于saltstack 3007.1版本 安装配置salt-api
keywords: alamlinux,saltstack，salt-api
mermaid: false
sequence: false
flow: false
mathjax: false
mindmap: false
mindmap2: false
---

基于salt 3007.1版本配置测试saltapi

# 1.salt-api说明

Salt-api其实是一个简单的salt web rest接口；可能通过这个api接口能完成命令行所有的操作；一般用于运维自动化平台的集成，操作方便；依赖如下：

- [**salt-api** using the CherryPy server](https://docs.saltproject.io/en/latest/ref/netapi/all/salt.netapi.rest_cherrypy.html#salt-api-using-the-cherrypy-server)

- [Using a WSGI-compliant web server](https://docs.saltproject.io/en/latest/ref/netapi/all/salt.netapi.rest_cherrypy.html#using-a-wsgi-compliant-web-server)

  

# 2. 背景

本文主要是参照官方文档在AlamLinux8 salt[3007.1](https://sysant.github.io/2024/08/04/saltstack-base-used/)版本安装部署salt-api服务，因为发现官方一些没有提到的点，踩了不少坑，才配置完成，早先版本没有出现过，搜索也没有发现类似问题，故记录下！

# 3. 安装salt-api服务

## 1). 检查salt-master主配置

```bash
$ egrep -v '^#|^$' /etc/salt/master
default_include: master.d/*.conf
user: root 
locale: zh_CN.UTF-8
worker_threads: 4 
file_roots:
  base:
    - /srv/salt
pillar_roots:
  base:
    - /srv/pillar
pillar_opts: True 
external_encoding: utf-8
```

## 2). 踩坑一

以上user: root要注意，这里如果是salt普通用户，会发现salt-api 起动会出问题如下：

```tex
$ tail -f /var/log/salt/api
    self.api = salt.netapi.NetapiClient(self.opts)
  File "/opt/saltstack/salt/lib/python3.10/site-packages/salt/netapi/__init__.py", line 79, in __init__
    self.key = salt.daemons.masterapi.access_keys(apiopts)
  File "/opt/saltstack/salt/lib/python3.10/site-packages/salt/daemons/masterapi.py", line 228, in access_keys
    key = mk_key(opts, user)
  File "/opt/saltstack/salt/lib/python3.10/site-packages/salt/daemons/masterapi.py", line 191, in mk_key
    with salt.utils.files.fopen(keyfile, "w+") as fp_:
  File "/opt/saltstack/salt/lib/python3.10/site-packages/salt/utils/files.py", line 388, in fopen
    f_handle = open(  # pylint: disable=resource-leakage,unspecified-encoding
PermissionError: [Errno 13] Permission denied: '/var/cache/salt/master/saltapi/.salt_key'
```

## 3). 配置salt-api自签名证书与私钥

这里用的是私有证书和自签名，如果是公有的申请的可以忽略

```bash
$ cd  /etc/salt/pki/
# 生成自签名证书
$ openssl req -x509 -nodes -days 3650 -newkey rsa:2048 -keyout saltapi.key -out saltapi.crt -subj "/CN=salt"
# 生成saltapi.key私钥
$ openssl genrsa -out saltapi.key 2048 
$ ls
master  minion  saltapi.key
# 基于saltapi.key 私钥，生成一个证书签名请求saltapi.csr文件（需要填写相应信息）
$ openssl req -new -key saltapi.key -out saltapi.csr
You are about to be asked to enter information that will be incorporated
into your certificate request.
What you are about to enter is what is called a Distinguished Name or a DN.
There are quite a few fields but you can leave some blank
For some fields there will be a default value,
If you enter '.', the field will be left blank.
-----
Country Name (2 letter code) [AU]:CN
State or Province Name (full name) [Some-State]:ShangHai
Locality Name (eg, city) []:HuangPu
Organization Name (eg, company) [Internet Widgits Pty Ltd]:Wapu
Organizational Unit Name (eg, section) []:infra
Common Name (e.g. server FQDN or YOUR name) []:saltapi
Email Address []:saltapi@test.com
Please enter the following 'extra' attributes
to be sent with your certificate request
A challenge password []:
An optional company name []:Test


# 生成一个自签名的证书 saltapi.crt
$ openssl x509 -req -days 3650 -in saltapi.csr -signkey saltapi.key -out saltapi.crt
Certificate request self-signature ok
subject=C = CN, ST = ShangHai, L = HuangPu, O = Test, OU = infra, CN = saltapi, emailAddress = saltapi@test.com

$ ls
master  minion  saltapi.crt  saltapi.csr  saltapi.key

# 签名证书验证
$ openssl x509 -in saltapi.crt -text -noout
Certificate:
    Data:
        Version: 1 (0x0)
        Serial Number:
            22:a3:26:bb:25:bf:94:95:20:ce:9a:a1:c6:35:d8:10:16:02:ca:a3
        Signature Algorithm: sha256WithRSAEncryption
        Issuer: C = CN, ST = ShangHai, L = HuangPu, O = Test, OU = infra, CN = saltapi, emailAddress = saltapi@test.com
        Validity
            Not Before: Sep 20 09:38:12 2024 GMT
            Not After : Sep 18 09:38:12 2034 GMT
        Subject: C = CN, ST = ShangHai, L = HuangPu, O = Test, OU = infra, CN = saltapi, emailAddress = saltapi@test.com
        Subject Public Key Info:
            Public Key Algorithm: rsaEncryption
                Public-Key: (2048 bit)
                Modulus:
                    …… 省略 ……
                Exponent: 65537 (0x10001)
    Signature Algorithm: sha256WithRSAEncryption
    Signature Value:
        bf:b7:8f:8f:45:c0:60:87:73:2d:4f:39:1d:ab:19:1e:33:00:
                   …… 省略 ……


```

以上表示私有自签证书配置完成！

## 4) . 创建saltapi认证账号

```bash
# 创建saltapi账号
$ useradd -s /usr/sbin/nologin saltapi
# 创建saltapi密码
$ passwd saltapi 
```

## 5). 配置salt-api

```bash
$ egrep -v '^#|^$' /etc/salt/master.d/salt-api.conf 
rest_cherrypy:
  port: 443 
  ssl_crt: /etc/pki/tls/certs/localhost.crt
  ssl_key: /etc/pki/tls/certs/localhost.key
external_auth:
  pam:
    saltapi:
      - .*
      - '@wheel'
      - '@runner'
      - '@jobs'
netapi_enable_clients:
  - local
  - local_async
  - local_batch
  - local_subset
  - runner
  - runner_async
log.error_file: /var/log/salt/api_error.log
log.debug_file: /var/log/salt/api_debug.log
log.level: info
token_expiration: 43200
```

以上配置和官方文档略有区别，如果完成按官方配置来，会有坑，因此

## 6). 踩坑二

以上配置主要在port 这里， 官方为8000 ，但如果我们用8000 会出现 如下错误：

```bash
$ curl -sSk https://localhost:8000/login -H 'Accept: application/x-yaml' -d username=saltapi -d password=saltapi -d eauth=pam
curl: (35) error:1408F10B:SSL routines:ssl3_get_record:wrong version number
```

而使用port 443后没有问题，再改回8000则不再有问题，不知道具体是什么原因，实测下来是这样！花了两天时间也没有找到为何！用了443就可以了！

```bash
$ curl -sSk https://localhost:8000/login -H 'Accept: application/x-yaml' -d username=saltapi -d password=saltapi -d eauth=pam
return:
- eauth: pam
  expire: 1726872153.4536295
  perms:
  - .*
  - '@jobs'
  - '@runner'
  - '@wheel'
  start: 1726828953.4536288
  token: 193882d7295aa8614a652ca54cf38e125d58df79
  user: saltapi
```

# 4. salt-api简单测试

## 1). 通过以上login后获取的token执行test.ping命令

```bash
$ curl -sSk https://localhost:8000  -H 'Accept: application/x-yaml'  -H 'X-Auth-Token: 193882d7295aa8614a652ca54cf38e125d58df79'    -d client=local  -d tgt='*' -d fun=test.ping
return:
- AlmaLinux8: true
  Rocky-9.2-test: true
  c29c521a73a3: false
  win-201602: true
  win2012: true
  win2016: true
```

## 2). 这里的执行方式说明如下：

```tex
local: 用于LocalClient向 Minions 发送命令。相当于saltCLI 命令。
runner:用于RunnerClient调用 Master 上的 runner 模块。相当于salt-runCLI 命令。
wheel:用于WheelClient调用 Master 上的 wheel 模块。Wheel 模块没有直接的 CLI 等效项，但它们通常管理 Master 端资源（例如状态文件、pillar 文件、Salt 配置文件），并公开与CLI 命令类似的功能。key wheel modulesalt-key
```

## 3). 异步执行并通过jid获取执行结果：

```bash
$ curl -sSk https://localhost:8000  -H 'Accept: application/x-yaml'  -H 'X-Auth-Token: 193882d7295aa8614a652ca54cf38e125d58df79'    -d client=local_async  -d tgt='*' -d fun=test.ping 
return:
- jid: '20240920105249623865'
  minions:
  - AlmaLinux8
  - c29c521a73a3
  - Rocky-9.2-test
  - win-201602
  - win2012
  - win2016
 # 通过jid获取异步执行结果
$ curl -sSk https://localhost:8000 -H 'Accept: application/json' -H "X-Auth-Token: 193882d7295aa8614a652ca54cf38e125d58df79" -d client='runner' -d tgt='*' -d fun='jobs.lookup_jid' -d jid='20240920105249623865'
{"return": [{"AlmaLinux8": true, "Rocky-9.2-test": true, "win-201602": true, "win2016": true, "win2012": true}]}
```

更多接口api使用参考官方文档