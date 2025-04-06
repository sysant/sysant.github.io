---
layout: post
title: kubernetes集群安装Addons组件
categories: [k8s,kubernetes,ingress,helm,openelb,metrics-server,krm]
description: kebernetes集群安装ingress,openelb,helm,metrics-server,krm组件
keywords: openelb,helm,ingress,metrics-server,krm大盘 
mermaid: false
sequence: false
flow: false
mathjax: false
mindmap: false
mindmap2: false
---

kubernetes集群安装Addons组件

# 1.openelb安装 ：
[官方参考文档](https://openelb.io/docs/getting-started/configuration/)：

github官方安装地址：
```
kubectl apply -f https://raw.githubusercontent.com/openelb/openelb/master/deploy/openelb.yaml
如果直接安装无法访问请下载来来，如果下载不了，联系我
wget https://raw.githubusercontent.com/openelb/openelb/master/deploy/openelb.yaml
```
或github官方
但需要下载镜像这里我已经反镜像下载好，并重新替换了， 放在[我的github](https://github.com/sysant/sysant.github.io/tree/master/k8s/openelb)中
下载到/root/openelb下：

安装openelb
```
cd /root/openelb
kubectl apply -f openelb.yaml
kubectl get pod -n openelb-system
```

![openelb](/images/k8s/addons/openelb01.png)

创建eip地址池，这里的地址要和节点地址一致，如我们集群节点ip段为 192.168.1.0/24
因此这里创建地址池：

```
# cat eip-pool.yaml
apiVersion: network.kubesphere.io/v1alpha2
kind: Eip
metadata:
    name: eip-pool
    annotations:
      eip.openelb.kubesphere.io/is-default-eip: "true"
spec:
    address: 192.168.1.70-192.168.1.90     # dhcp保留地址
    priority: 100
    disable: false
    protocol: layer2
    interface: enp0s3                      # 节点网卡可通过ip link show查看
```

验证安装nginx服务
```
kubectl create deployment demoapp --image=registry.cn-hangzhou.aliyuncs.com/san2005/public:nginx_lts --replicas=2
```

基于openelb创建LoadBalancer类似service

```
cat demoapp.yaml 
apiVersion: v1
kind: Service
metadata:
  name: demoapp
  annotations:
    lb.kubesphere.io/v1alpha1: openelb
spec:
  type: LoadBalancer
  ports:
  - port: 80
    targetPort: 80
    selector:
    app: demoapp
```

```
kubectl apply -f demoapp.yaml
kubectl get svc demoapp

NAME      TYPE           CLUSTER-IP     EXTERNAL-IP    PORT(S)        AGE
demoapp   LoadBalancer   10.96.106.55   192.168.1.71   80:30599/TCP   16m
```

可以看到已经获取了ip　 192.168.1.71
浏览器访问http://192.168.1.71

# 2.安装helm
[官方安装参考文档](https://helm.sh/docs/) 
[Helm客户端安装](https://helm.sh/docs/intro/install/)

```
wget https://get.helm.sh/helm-v3.17.2-linux-amd64.tar.gz
tar xvf helm-v3.17.2-linux-amd64.tar.gz -C /usr/local/bin/
```
[Helm Charts仓库](https://artifacthub.io/)
添加bitnami和官方helm仓库： 

```
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo add stable https://charts.helm.sh/stable
```

Helm 简单使用:
查询包：

```
helm search repo bitnami/redis
查询历史版本：
helm search repo bitnami/redis -l 或 --versions
下载版本：
helm pull bintnami/xxx  --version 版本
安装 包(名称空间隔离性)：
helm install -n NS xxx .
查看：
helm list -n ns
更新配置： helm upgrade -n NS  xxx包 .
```

# 3.ingress安装
yaml直接安装
```
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.12.0/deploy/static/provider/cloud/deploy.yaml
```

[安装yam文件](https://kubernetes.github.io/ingress-nginx/deploy/)
[官方使用示例](https://github.com/kubernetes/ingress-nginx)

这里通过helm安装

```
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm repo update
helm pull  ingress-nginx/ ingress-nginx
tar xvf ingress-nginx-4.12.0.tgz
cd ingress-nginx/
vim values.yaml  #　先将里面的镜像手动下载传到个人仓库中
```

如果以上下载慢或无法下载
[这里下载](https://github.com/sysant/sysant.github.io/blob/master/k8s/ingress/ingress-nginx.tar.gz)
vlues.yaml中的镜像可以直接替换后类似如下：

```
cat values.yaml |egrep "image:|registry:"|grep -v "#"
  image:
    registry: registry.k8s.io
  image:
    registry: registry.cn-hangzhou.aliyuncs.com
    image: san2005/public
      image:
        registry: registry.cn-hangzhou.aliyuncs.com
        image: san2005/public
  image:
    image: defaultbackend-amd64

cd ingress-nginx/   vlues.yaml所在目录
kubectl create ns  ingress-nginx
helm install ingress-nginx -n ingress-nginx . 
[root@k8s-master01 ingress-nginx]# kubectl get svc -n ingress-nginx
```

![ingress](/images/k8s/addons/ingress.png)

# 4.安装metrics-server
[官方文档](https://github.com/kubernetes-sigs/metrics-server)
安装 ：

```
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
```

或者直接从我的github中安装 ：区别在于里面的镜像替换成阿里云镜像
```
kubectl apply -f https://raw.githubusercontent.com/sysant/sysant.github.io/refs/heads/master/k8s/metrics-server/metrics-server.yaml
kubectl get pod  -n kube-system -l k8s-app=metrics-server
```

![metrics-server](/images/k8s/addons/metrics-server.png)

``` kubectl top node```

![metrics-server02](/images/k8s/addons/metrics-server02.png)

# 5.KRM大盘安装 

k８s官方dashboard功能较强弱,第三方有很多,这里参考杜宽[大佬的ＫＲＭ](https://gitee.com/dukuan/krm)

```
kubectl create ns krm
kubectl create sa krm-backend -n krm
kubectl create rolebinding krm-backend --clusterrole=edit --serviceaccount=krm:krm-backend --namespace=krm
kubectl create clusterrole namespace-creater --verb=create --resource=namespaces
 kubectl create clusterrolebinding krm-backend-ns-creater --clusterrole=namespace-creater --serviceaccount=krm:krm-backend --namespace=krm
```
生成密码：

```
echo -n "admin" |md5sum |tr a-z A-Z

21232F297A57A5A743894A0E4A801FC3  -
```

部署后端 服务

```
cat <<EOF | kubectl -n krm apply -f -
---
apiVersion: v1
kind: Service
metadata:
  labels:
    app: krm-backend
  name: krm-backend
spec:
  ports:
  - name: http
    port: 8080
    protocol: TCP
    targetPort: 8080
  selector:
    app: krm-backend
  sessionAffinity: None
  type: ClusterIP
---
apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    app: krm-backend
  name: krm-backend
spec:
  replicas: 1
  selector:
    matchLabels:
      app: krm-backend
  strategy:
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
    type: RollingUpdate
  template:
    metadata:
      labels:
        app: krm-backend
    spec:
      serviceAccountName: krm-backend
      containers:
      - env:
        - name: TZ
          value: Asia/Shanghai
        - name: LANG
          value: C.UTF-8
        - name: GIN_MODE
          value: release
        - name: LOG_LEVEL
          value: info
        - name: USERNAME
          value: 21232F297A57A5A743894A0E4A801FC3    可替换，换上面的方面生成md5值
        - name: PASSWORD
          value: 21232F297A57A5A743894A0E4A801FC3
        - name: "IN_CLUSTER"
          value: "true"
        image: registry.cn-beijing.aliyuncs.com/dotbalo/krm-backend:latest
        lifecycle: {}
        livenessProbe:
          failureThreshold: 2
          initialDelaySeconds: 10
          periodSeconds: 10
          successThreshold: 1
          tcpSocket:
            port: 8080
          timeoutSeconds: 2
        name: krm-backend
        ports:
        - containerPort: 8080
          name: web
          protocol: TCP
        readinessProbe:
          failureThreshold: 2
          initialDelaySeconds: 10
          periodSeconds: 10
          successThreshold: 1
          tcpSocket:
            port: 8080
          timeoutSeconds: 2
        resources:
          limits:
            cpu: 1
            memory: 1024Mi
          requests:
            cpu: 200m
            memory: 256Mi
      restartPolicy: Always
EOF
```

部署前端服务

```
cat<<EOF | kubectl -n krm apply -f -
---
apiVersion: v1
kind: Service
metadata:
  labels:
    app: krm-frontend
  name: krm-frontend
spec:
  ports:
  - name: http
    port: 80
    protocol: TCP
    targetPort: 80
  selector:
    app: krm-frontend
  sessionAffinity: None
  type: NodePort
---
apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    app: krm-frontend
  name: krm-frontend
spec:
  replicas: 1
  selector:
    matchLabels:
      app: krm-frontend
  strategy:
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
    type: RollingUpdate
  template:
    metadata:
      labels:
        app: krm-frontend
    spec:
      containers:
      - env:
        - name: TZ
          value: Asia/Shanghai
        - name: LANG
          value: C.UTF-8
        image: registry.cn-beijing.aliyuncs.com/dotbalo/krm-frontend:latest
        lifecycle: {}
        livenessProbe:
          failureThreshold: 2
          initialDelaySeconds: 10
          periodSeconds: 10
          successThreshold: 1
          tcpSocket:
            port: 80
          timeoutSeconds: 2
        name: krm-backend
        ports:
        - containerPort: 80
          name: web
          protocol: TCP
        readinessProbe:
          failureThreshold: 2
          initialDelaySeconds: 10
          periodSeconds: 10
          successThreshold: 1
          tcpSocket:
            port: 80
          timeoutSeconds: 2
        resources:
          limits:
            cpu: 1
            memory: 512Mi
          requests:
            cpu: 100m
            memory: 256Mi
      restartPolicy: Always
 EOF
```

检查安装：

```
kubectl get po -n krm
kubectl get svc -n krm
```

krm 登录 http://192.168.1.101:32649/
![krm01](/images/k8s/krm01.png)
![krm02](/images/k8s/krm02.png)

用户名密码Admin admin 
登录 后添加集群
![krm03](/images/k8s/krm03.png)
![krm04](/images/k8s/krm04.png)

将krm访问地址通过openelb组件功能访问：
```
# kubectl edit svc krm-frontend -n krm
将 type: NodePort 修改为 LoadBalancer
添加注解：
metadata:
  annotations:
    lb.kubesphere.io/v1alpha1: openelb
保存退出
kubectl get svc  -n krm
```
![krm05](/images/k8s/krm05.png)

此时可以直接通过 http://192.168.1.73访问：

![krm06](/images/k8s/krm06.png)
到此以上5个功能组件安装完成！
