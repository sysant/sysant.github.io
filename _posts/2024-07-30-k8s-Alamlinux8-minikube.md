---
layout: post
title: Alamlinux8使用minikube搭建单机k8s测试环境
categories: [51cto老博文]
description: Alamlinux8 通过minikub部署单机测试k8s环境
keywords: alamlinux，k8s, minikube
mermaid: false
sequence: false
flow: false
mathjax: false
mindmap: false
mindmap2: false
---

基于Alamlinux8 通过minikube搭建单机k8s测试环境

一、什么是minikube
-----------


* [minikube](https://minikube.sigs.k8s.io/docs/start/)是一个开源工具，用于在本地开发环境中快速搭建一个单机节点的Kubernetes集群。从而提供一个容器化的运行环境。
* 支持多种虚拟化技术，在不同平台上都可以运行，如虚拟主机、VirtualBox、Hyper\-V、KVM等。
* 通过Minikube，开发人员可以方便地在本地环境中测试、构建和部署应用程序，并尝试不同的Kubernetes功能和配置。
* Minikube提供了一些命令行工具，如kubectl，用于与Kubernetes集群进行交互，可以在本地开发中提高效率和便捷性。
* 测试环境需要满足如下要求：  

2 CPUs or more  
2GB of free memory  
20GB of free disk space  
Internet connection  
Container or virtual machine manager, such as: Docker, QEMU, Hyperkit, Hyper\-V, KVM, Parallels, Podman, VirtualBox, or VMware Fusion/Workstation

二、本次测试环境

alamlinux8.8 minikube-1.31.2 docker-ce-24.0.6-1  

**1、安装docker\-ce**


```
[root@AlmaLinux8 tmp]# wget http://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo -O /etc/yum.repos.d/docker-ce.repo
[root@AlmaLinux8 tmp]# yum list docker-ce --showduplicates | sort -r |head -n 3
docker-ce.x86_64                3:24.0.6-1.el8                  docker-ce-stable
docker-ce.x86_64                3:24.0.5-1.el8                  docker-ce-stable
docker-ce.x86_64                3:24.0.4-1.el8                  docker-ce-stable
[root@AlmaLinux8 tmp]# yum install -y docker-ce-24.0.6-1.el8

[root@AlmaLinux8 tmp]# systemctl start docker
[root@AlmaLinux8 tmp]# systemctl status docker
● docker.service - Docker Application Container Engine
   Loaded: loaded (/usr/lib/systemd/system/docker.service; disabled; vendor preset: >
   Active: active (running) since Sun 2023-10-08 16:06:20 CST; 14s ago
     Docs: https://docs.docker.com
 Main PID: 48525 (dockerd)

 [root@AlmaLinux8 tmp]# systemctl enable docker
Created symlink /etc/systemd/system/multi-user.target.wants/docker.service → /usr/lib/systemd/system/docker.service.

[root@AlmaLinux8 tmp]# docker --version
Docker version 24.0.6, build ed223bc
```

**2、配置docker镜像加速服务**  

这里使用[阿里云](https://cr.console.aliyun.com/cn-hangzhou/instances/mirrors)镜像个人加速服务；  

阿里云提供的Docker镜像加速器（Docker Registry Mirror）支持公共云、专有云和混合云等多种环境，包括国内和全球范围的镜像仓库。用户可以免费获取加速器地址并使用其服务。如果没有账号，可以注册下；  

注册阿里云账户后，访问阿里云控制台中搜索的"容器镜像服务"，镜像工具中，生成个人专属的加速器地址。  

![Alamlinux8使用minikube搭建单机k8s测试环境](/images/Alamlinux8使用minikube搭建单机k8s测试环境/Alamlinux8使用minikube搭建单机k8s测试环境_nginx.png)

将加速地址配置添加到Docker配置文件的registry-mirrors字段中,重启Docker客户端，即可享受阿里云Docker镜像加速器的服务。如下：

![Alamlinux8使用minikube搭建单机k8s测试环境](/images/Alamlinux8使用minikube搭建单机k8s测试环境/Alamlinux8使用minikube搭建单机k8s测试环境_nginx_02.png)

重启docker服务


```
systemctl daemon-reload
systemctl restart docker

```

**3、安装minikube**


```
[root@AlmaLinux8 tmp]# curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-latest.x86_64.rpm

[root@AlmaLinux8 tmp]# rpm -Uvh minikube-latest.x86_64.rpm
sudo sysctl fs.protected_regular=0

echo "fs.protected_regular=0" >>/etc/sysctl.conf

```

**4、minikube安装单节点k8s集群**


```
[root@AlmaLinux8 cache]# minikube start --force --driver=docker --image-repository=registry.cn-hangzhou.aliyuncs.com/google_containers
* Almalinux 8.8 上的 minikube v1.31.2
! 当提供 --force 参数时，minikube 将跳过各种验证，这可能会导致意外行为
* 根据现有的配置文件使用 docker 驱动程序
* The "docker" driver should not be used with root privileges. If you wish to continue as root, use --force.
* 如果您在VM中运行 minikube，请考虑使用 --driver=none:
*   https://minikube.sigs.k8s.io/docs/reference/drivers/none/
* 提示：要删除此 root 拥有的集群，请运行：sudo minikube delete
* 正在集群 minikube 中启动控制平面节点 minikube
* 正在拉取基础镜像 ...
* 正在更新运行中的 docker "minikube" container ...
    > kubectl.sha256:  64 B / 64 B [-------------------------] 100.00% ? p/s 0s
    > kubeadm.sha256:  64 B / 64 B [-------------------------] 100.00% ? p/s 0s
    > kubelet.sha256:  64 B / 64 B [-------------------------] 100.00% ? p/s 0s
    > kubectl:  1.39 MiB / 46.98 MiB [>________] 2.96% 18.26 KiB p/s ETA 42m36s
    > kubelet:  3.83 MiB / 101.25 MiB [>_____] 3.79% 22.89 KiB p/s ETA 1h12m37s
    > kubeadm:  21.96 MiB / 45.93 MiB [--->___] 47.81% 168.60 KiB p/s ETA 2m25s
  - 正在生成证书和密钥...
  - 正在启动控制平面...
  - 配置 RBAC 规则 ...
* 配置 bridge CNI (Container Networking Interface) ...
  - 正在使用镜像 registry.cn-hangzhou.aliyuncs.com/google_containers/storage-provisioner:v5
* 正在验证 Kubernetes 组件...
* 启用插件： storage-provisioner, default-storageclass
* kubectl not found. If you need it, try: 'minikube kubectl -- get pods -A'
* 完成！kubectl 现在已配置，默认使用"minikube"集群和"default"命名空间

```

**5、下载安装kubectl**  

原生kubectl工具


```
[root@AlmaLinux8 cache]# curl -Lo kubectl   http://kubernetes.oss-cn-hangzhou.aliyuncs.com/kubernetes-release/release/v1.22.1/bin/linux/amd64/kubectl
[root@AlmaLinux8 cache]# mv kubectl /usr/bin
[root@AlmaLinux8 cache]# chmod a+x /usr/bin/kubectl

[root@AlmaLinux8 cache]# kubectl version
Client Version: version.Info{Major:"1", Minor:"22", GitVersion:"v1.22.1", GitCommit:"632ed300f2c34f6d6d15ca4cef3d3c7073412212", GitTreeState:"clean", BuildDate:"2021-08-19T15:45:37Z", GoVersion:"go1.16.7", Compiler:"gc", Platform:"linux/amd64"}
Server Version: version.Info{Major:"1", Minor:"27", GitVersion:"v1.27.4", GitCommit:"fa3d7990104d7c1f16943a67f11b154b71f6a132", GitTreeState:"clean", BuildDate:"2023-07-19T12:14:49Z", GoVersion:"go1.20.6", Compiler:"gc", Platform:"linux/amd64"}
WARNING: version difference between client (1.22) and server (1.27) exceeds the supported minor version skew of +/-1

[root@AlmaLinux8 cache]# 创建kubectl别名
[root@AlmaLinux8 cache]## alias kubectl="minikube kubectl --"

检查安装版本
[root@AlmaLinux8 cache]# kubectl get pods -A
NAMESPACE     NAME                               READY   STATUS    RESTARTS        AGE
kube-system   coredns-65dcc469f7-d92fr           1/1     Running   0               4m24s
kube-system   etcd-minikube                      1/1     Running   0               4m36s
kube-system   kube-apiserver-minikube            1/1     Running   0               4m36s
kube-system   kube-controller-manager-minikube   1/1     Running   0               4m36s
kube-system   kube-proxy-7xk7l                   1/1     Running   0               4m24s
kube-system   kube-scheduler-minikube            1/1     Running   0               4m37s
kube-system   storage-provisioner                1/1     Running   1 (4m22s ago)   4m34s

以上说明minikube单机k8s测试集群安装完成！

```

**6、补充minikube命令**


```
# 检查安装结果
minikube help
minikube status
kubectl version
kubectl get nodes
kubectl get pods -A

# 查询运行的 pod
minikube kubectl -- get po -A

# 挂起虚拟机
minikube pause

# 停止虚拟机
minikube stop

# 修改虚拟机内存配置
minikube config set memory 16384

# 查看 minikube 的安装目录列表
minikube addons list

# 启动 dashboard 控制台
minikube dashboard
curl 127.0.0.1:23341

# 删除所有 minikube 虚拟机
minikube delete --all

# 部署目录
/var/lib/kubelet
/var/lib/minikube

# 使用minikube导入镜像,当本地镜像总是无法找到时，可以留意这个这种方式
minikube load xxx.tar

```

**7、开启dashboard**


```
[root@AlmaLinux8 ~]# minikube dashboard --url
* 正在验证 dashboard 运行情况 ...
* 正在启动代理...
* 正在验证 proxy 运行状况 ...
http://127.0.0.1:35837/api/v1/namespaces/kubernetes-dashboard/services/http:kubernetes-dashboard:/proxy/
此时不能外部访问；可以通过kubectl proxy代理对外，配置如下：
主机ip：172.21.161.234
[root@AlmaLinux8 ~]# kubectl proxy --port=8000 --address='172.21.161.234' --accept-hosts='^.*' &

同时关闭firewalled 
[root@AlmaLinux8 ~]#  systemctl stop firewalld
[root@AlmaLinux8 ~]#  systemctl disable firewalld

```

通过浏览器再次访问dashboard：  

[http://172.21.161.234:8000/api/v1/namespaces/kubernetes-dashboard/services/http:kubernetes-dashboard:/proxy/#/clusterrole?namespace=default](http://172.21.161.234:8000/api/v1/namespaces/kubernetes-dashboard/services/http:kubernetes-dashboard:/proxy/#/clusterrole?namespace=default)  

如图：  

![Alamlinux8使用minikube搭建单机k8s测试环境](/images/Alamlinux8使用minikube搭建单机k8s测试环境/Alamlinux8使用minikube搭建单机k8s测试环境_docker_03.png)


deployment测试
------------


通过deployment拉起一个pod包含两个nginx容器  

[root@AlmaLinux8 k8s]# cat nginx-deployment.yaml


```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
  labels:
    app: nginx
spec:
  replicas: 1 
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:latest
        imagePullPolicy: IfNotPresent 
        ports:
        - containerPort: 80

```

应用yaml文件


```
[root@AlmaLinux8 k8s]# kubectl apply -f nginx-deployment.yaml 
deployment.apps/nginx-deployment created
[root@AlmaLinux8 k8s]# kubectl get pod
NAME                                READY   STATUS    RESTARTS   AGE
nginx-deployment-7777f55dd5-rnpld   1/1     Running   0          4s
[root@AlmaLinux8 k8s]# kubectl get pod
NAME                                READY   STATUS    RESTARTS   AGE
nginx-deployment-7777f55dd5-rnpld   1/1     Running   0          6s

```

临时手动将nginx端口对外开放


```
[root@AlmaLinux8 k8s]# kubectl port-forward nginx-deployment-7777f55dd5-rnpld  --address=0.0.0.0 8080:80
Forwarding from 0.0.0.0:8080 -> 80

```

浏览器访问http://172.21.161.234:8080/  

![Alamlinux8使用minikube搭建单机k8s测试环境](/images/Alamlinux8使用minikube搭建单机k8s测试环境/Alamlinux8使用minikube搭建单机k8s测试环境_nginx_04.png)


留过思考题：如何通过修改deployment配置文件，直接暴露nginx web 服务？


以上deployment拉起容器只是抛砖引玉的效果， 更多k8s学习请参考：  

[minikube官网](https://minikube.sigs.k8s.io)  

[kubernetes文档](http://kubernetes.p2hp.com/docs/setup/learning-environment/)


