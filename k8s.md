帮助文档explain

```shell
查看Pod的yaml文件可以配哪些字段
kubectl explain pods
```

详细信息describe

```shell
如果pod启动失败，使用describe查询详细信息
kubectl describe pods pod_name -n dev
```

监控内容变换-w

```shell
在任何命令后面加上-w
kubectl get pods -n dev -w
```

查看信息

```shell
kubectl get deploy,rs,pod -n dev
```

