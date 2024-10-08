---
layout: post
title: 从镜像制作管理到k8s调度运行
categories: [51cto老博文]
description: 程序从docker容器运行，到制作镜像，再到k8s运行管理
keywords: docker，k8s，容器，容器镜像制作
mermaid: false
sequence: false
flow: false
mathjax: false
mindmap: false
mindmap2: false
---

程序从docker容器运行到制作镜像，再到k8s运行管理过程


一、前言

### 1、简介

上文基于alamlinux8系统和minikube搭建单机k8s集群，本文主要记录下从镜像制作与管理到上K8s的过程；从中可以大概了解业务代码到镜像、容器、镜像仓库、docker运行、k8s集群之间的关系，以及deployment用法初探；有助于进一步理解业务上k8s的过程；

  


### 2、镜像与容器

简单的说docker镜像没有运行之前就是一个文件系统，运行起来之后就被叫做容器。镜像是创建容器的模板；

### 3、docekr与k8s

Docker是容器运行管理的载体，只是容器的一种，它面向的是单体(机)，K8S可以管理多种容器(pod管理)，它面向的是集群，Docker可以作为一种容器方案被K8S管理。

### 4、镜像仓库

用于存放管理镜像；镜像需要根据业务用途制作；可用于多机，多地多环境之间分享管理镜像；上传(push)，下载（push）镜像；

本文演示的主要内容如下：

![从镜像制作管理到k8s调度运行_docker](/images/从镜像制作管理到k8s调度运行/从镜像制作管理到k8s调度运行_docker.png)

二、Dockerfile制作镜像与上传仓库
---------------------

[镜像内的程序](https://github.com/sysant/Strudy_Tornado.git)：主要基于python3\.6\.8镜像，python tornado == 6\.1模块；用来实现前后端交互生成球的简单web程序；

### 1、安装docker

参考另一篇博文[《Alamlinux8使用minikube搭建单机k8s测试环境》](https://blog.51cto.com/dyc2005/7792135)这里不再演示！

### 2、拉取代码到本地：

```bash
$ git clone  https://github.com/sysant/Strudy_Tornado.git
$ cd Strudy_Tornado/ShuangSeQiu
$ ls
demo_jpg  qiu.py Dockerfile  REDME.txt  requirements.txt  start.sh  static  templates
# 查看Dockerfile内容
$ cat Dockerfile* 

```
### 3、编写Dockerfile

```bash
FROM python:3.6.8
WORKDIR ./ShuangSeQiu
ADD . .
RUN pip3 install -r requirements.txt
EXPOSE 10800
#CMD ["python", "./qiu.py"]
ENTRYPOINT ["python", "./qiu.py"]

```
### 4、制作镜像

```bash
#制作镜像，注意本地要安装配置python3.6.8 且安装好pip3
$ docker build -t qiu:v1.0 .
Sending build context to Docker daemon  195.1kB
Step 1/6 : FROM python:3.6.8
 ---> 48c06762acf0
Step 2/6 : WORKDIR ./ShuangSeQiu
 ---> Using cache
 ---> 72c2d7d8ccdb
Step 3/6 : ADD . .
 ---> 8079d650180a
Step 4/6 : RUN pip3 install -r requirements.txt
 ---> Running in e8e99451139f
Collecting tornado==6.1 (from -r requirements.txt (line 1))
  Downloading https://files.pythonhosted.org/packages/85/26/e710295dcb4aac62b08f22d07efc899574476db37532159a7f71713cdaf2/tornado-6.1-cp36-cp36m-manylinux2010_x86_64.whl (427kB)
Installing collected packages: tornado
Successfully installed tornado-6.1
WARNING: You are using pip version 19.1.1, however version 21.3.1 is available.
You should consider upgrading via the 'pip install --upgrade pip' command.
Removing intermediate container e8e99451139f
 ---> bb841ce7c4ad
Step 5/6 : EXPOSE 10800
 ---> Running in af27ebd9b224
Removing intermediate container af27ebd9b224
 ---> d85c03453c4e
Step 6/6 : ENTRYPOINT ["python", "./qiu.py"]
 ---> Running in 8a66d225ccd2
Removing intermediate container 8a66d225ccd2
 ---> cc822b291e8b
Successfully built cc822b291e8b
Successfully tagged qiu:v1.0

# 查看
$ docker images 
REPOSITORY                   TAG       IMAGE ID       CREATED          SIZE
qiu                          v1.0      cc822b291e8b   38 seconds ago   932MB


```
### 5、上传镜像

```
# 登录镜像仓库；阿里云仓库
$ docker login --username=USER@aliyun.com registry.cn-hangzhou.aliyuncs.com*

```
![从镜像制作管理到k8s调度运行_k8s_02](/images/从镜像制作管理到k8s调度运行/从镜像制作管理到k8s调度运行_k8s_02.png)

对镜像qiu:v1\.0打tag并上传

```bash
$ docker tag cc822b291e8b registry.cn-hangzhou.aliyuncs.com/san2005/study:qiu_v1.0
```
三、docker单机运行
------------

### 1、通过docker运行

```bash
# 运行镜像生成运行容器
$ docker run -d -p 10800:10800 qiu:v1.0

#查看运行容器
$ docker ps -a
CONTAINER ID   IMAGE          COMMAND         CREATED       STATUS         PORTS                                           NAMES
d22b718a93e9   qiu:v1.0    "python ./qiu.py"  1 min ago    Up 2 days      0.0.0.0:10800->10800/tcp, :::10800->10800/tcp   hungry_franklin
```
![从镜像制作管理到k8s调度运行_仓库_03](/images/从镜像制作管理到k8s调度运行/从镜像制作管理到k8s调度运行_仓库_03.png)

docker容器已经通过镜像成功运行且开放了端口10800

### 2、访问验证

curl http://172\.21\.161\.185:10800

![从镜像制作管理到k8s调度运行_镜像_04](/images/从镜像制作管理到k8s调度运行/从镜像制作管理到k8s调度运行_仓库_04.png)

![从镜像制作管理到k8s调度运行_镜像_05](/images/从镜像制作管理到k8s调度运行/从镜像制作管理到k8s调度运行_镜像_05.png)

此时，可以通过docker上的主机ip 访问容器中的程序；但问题是docker上运行是单机的， docker程序或容器岩机后，业务将无法访问；

  


四、K8s集群运行
---------

### 1、创建secrets

由于镜像获取需要仓库的登录认证，因些在编写deployment之前先要创建secret控制器

脚本内容用户名和密码需要替换成对应的阿里账号和密码

```bash
$ cat ali-secret.sh
#!/bin/sh
kubectl create secret docker-registry registry-ali-hz --namespace=default --docker-server=registry.cn-hangzhou.aliyuncs.com --docker-username=USER@aliyun.com --docker-password=PASSWORD

```
![从镜像制作管理到k8s调度运行_docker_06](/images/从镜像制作管理到k8s调度运行/从镜像制作管理到k8s调度运行_docker_06.png)

secret创建完成！

  


### 2、编写业务deployment

cat qiu\-deployment.yaml

```bash
apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    app: qiu-deployment
  name: qiu-deployment
spec:
  replicas: 2 
  selector:
    matchLabels:
      app: qiu-deployment
  strategy: {}
  template:
    metadata:
      labels:
        app: qiu-deployment
    spec:
      imagePullSecrets:
      # secrets 需要先创建好
      - name: registry-ali-hz
      containers:
      - name: qiu
        image: registry.cn-hangzhou.aliyuncs.com/san2005/study:qiu_v1.0
```

```bash
# 应用qiu-deployment.yaml
$ kubectl alloy -f qiu-deployment.yaml
deployment.apps/qiu-deployment created
# 查看生成的deployment

```
![从镜像制作管理到k8s调度运行_k8s_07](/images/从镜像制作管理到k8s调度运行/从镜像制作管理到k8s调度运行_k8s_07.png)

至此生成双色班的后端程序从镜像里生成了两个pod(每个pod一个容器)，并且都运行卫qiu.py程序(开放了端口10800）但些时只有pod内部能访问

### 3、编写service

前面用`Deployment`部署好了应用，但应用`Pod`不能直接对外提供服务；我们需要加上`Service`，才能让外部请求能访问到`Kubernetes`集群里的应用，并为`Pod`提供负载均衡；

下面是`Service`对象的常用属性设置：

* 使用label selector，在集群中查找目标`Pod`;
* ClusterIP设置Service的集群内IP让`kube-proxy`使用;
* 通过prot和targetPort将访问端口与目标端口建议映射（不指定targetPort时默认值和port设置的值一样）;
* Service支持多个端口映射
* Service支持HTTP（默认），TCP和UDP协议;

针对上面的deployment业务的service如下：

cat qiu\-service.yaml

```bash
apiVersion: v1
kind: Service
metadata:
  namespace: default
  name: qiu-deployment
  labels:
    app: qiu-deployment
spec:
  # if your cluster supports it, uncomment the following to automatically create
  # an external load-balanced IP for the frontend service.
  # type: LoadBalancer
  #type: LoadBalancer
  ports:
  - port: 10800
    protocol: TCP
    targetPort: 10800
  selector:
    app: qiu-deployment
  type: NodePort
```
查看service生成情况：

![从镜像制作管理到k8s调度运行_python_08](/images/从镜像制作管理到k8s调度运行/从镜像制作管理到k8s调度运行_python_08.png)

至此生成了时可理解为pod的cluster\-ip:10800 能访问pod中容器(一台或多台) 10080；但cluster\-ip不能对外部访问；可以通过node节点ip访问30590访问：

curl [http://192.168.85.2:31509](http://192.168.85.2:31509)

![从镜像制作管理到k8s调度运行_仓库_09](/images/从镜像制作管理到k8s调度运行/从镜像制作管理到k8s调度运行_仓库_09.png)

说明：通过minikube service 查看出qiu\-deployment的node访问地址，也可以通过等同 kubectl describe pod qiu\-deployment\-8557879b78\-ntlbl \|grep Node；再结合svc上与pod映射的端口  即192.168.85.2:31590进行访问。

这里的nodePort访问只针对集群可以访问；或node本机能访问；k8s集群内部能访问；如果是互联网其他机器访问；需要ingress或外层再加一个LB代理；这里通过kubectl port\-forward命令进行模块

### 4、业务访问验证

```bash
$ kubectl port-forward --address=0.0.0.0 service/qiu-deployment 10800:10800
Forwarding from 0.0.0.0:10800 -> 10800

#查看本机的网卡地址 172.21.161.234
$ hostname -I
172.21.161.234 172.17.0.1 192.168.85

```
浏览器访问[http://172.21.161.234:10800](http://172.21.161.234:10800)

![从镜像制作管理到k8s调度运行_k8s_10](/images/从镜像制作管理到k8s调度运行/从镜像制作管理到k8s调度运行_k8s_10.png)

![从镜像制作管理到k8s调度运行_k8s_11](/images/从镜像制作管理到k8s调度运行/从镜像制作管理到k8s调度运行_k8s_11.png)

验证通过service访问的负载均衡

```bash
[root@AlmaLinux8 qiu]# kubectl logs -f qiu-deployment-8557879b78-rrvhw
[I 231018 09:47:23 web:2243] 200 GET / (10.244.0.1) 6.25ms
[I 231018 09:47:25 web:2243] 200 GET / (10.244.0.1) 1.85ms

[root@AlmaLinux8 qiu]# kubectl logs -f qiu-deployment-8557879b78-lgs2g
[I 231018 09:47:48 web:2243] 200 GET / (10.244.0.1) 6.62ms
```
访问多次后，会发现后端pod都有收到请求！

  


五、总结
----

通过研发代码编写，生成镜像（研发或运维），上传私有仓库，线上主机基于k8s集群控制器deployment运行，并通过sevice，nodeport对外发布；希望本文对初学者在大方向上能对业务上k8s有一定的了解；如有不当之处欢迎指正！
