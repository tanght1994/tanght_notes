# 安装

```shell
sudo apt-get update
sudo apt-get install apt-transport-https ca-certificates curl software-properties-common

# 添加Docker官方GPG key
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

# 添加Docker稳定版仓库
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"

sudo apt-get update
sudo apt-get install docker-ce
sudo docker run hello-world
```

加速

Ubuntu/Centos相同

```bash
/etc/docker/daemon.json
{
	"registry-mirrors":["http://f1361db2.m.daocloud.io"]
}
```

# 帮助

输出所有命令`docker --help`

```shell
# 输出帮助信息
docker --help
# 输出docker run 命令的帮助
docker run --help
# 输出docker的network命令的create命令的帮助
docker network create --help
```

# 简介

docker run会运行一个容器，镜像被制作出来的时候会指定容器启动时运行的第一条命令，此命令结束意味着此容器结束。

有些镜像（比如干净的Centos镜像）的第一条命令是/bin/bash，所以这样的容器run起来的时候，0.0001秒就结束了，因为/bin/bash这个命令0.00001秒就执行完了。这种镜像一般是被当作基础镜像，没人会run一个启动命令是/bin/bash的镜像。

有些镜像的第一条命令是启动一个服务，比如Mysql镜像，这个启动命令是一个死循环，永远不会结束，所以这样的容器run起来的时候，不会立即结束，可以持续的对外提供服务。当到收到stop信号，或者Mysql有BUG崩溃了的时候，此命令结束，容器结束。

# 命令

## 创建容器

语法：`docker create [OPTIONS] IMAGE [COMMAND] [ARG...]`

返回容器ID

```shell
# 根据imageID这个镜像，创建一个容器
docker create imageID

# 根据imageID这个镜像，创建一个容器，并命名为mytest（docker ps的时候，NAME字段显示为mytest）
docker create --name mytest imageID
```

## 运行容器

语法：`docker start`

## 创建并运行容器

语法：`docker run`

其作用相当于`docker create` + `docker start`

## 查看容器

语法：`docker ps`

## 查看镜像

```shell
docker images
```

## 拉取镜像

```shell
docker pull nginx # 拉取最新版本的nginx
docker pull nginx:latest # 拉取最新版本的nginx
docker pull nginx:1.0.0 # 拉取1.0.0版本的nginx
```

## 运行容器

```shell
# 根据imageID这个镜像，创建一个新容器，并运行容器
# -it提供交互终端
# -p 8000:80  将主机的8000端口映射到容器的80端口
docker run --name haha -p 8000:80 -it imageID command

# --name tht_nginx    docker ps的时候会显示tht_nginx这个名字用以提示
# -p 8080:80    将主机的8080端口映射到本容器的80端口（主机的8080端口与容器的80端口绑定到一起了，成为一体了）
# -d 容器以后台程序运行，不提供交互终端
docker run --name tht_nginx -p 8080:80 -d f35646e83998
```

容器

```shell
docker run --name haha -p 8000:80 imageID

# --name tht_nginx    docker ps的时候会显示tht_nginx这个名字用以提示
# -p 8080:80    将主机的8080端口映射到本容器的80端口（主机的8080端口与容器的80端口绑定到一起了，成为一体了）
# -d 容器以后台程序运行，不提供交互终端
docker run --name tht_nginx -p 8080:80 -d f35646e83998
docker run --name tht_nginx -p 8080:80 -d f35646e83998
docker container run -it ubuntu bash



# 启动已经停止了的容器
docker start 容器ID

# 列出正在运行的容器
docker ps
# 列出所有容器，包括已经停止了的容器
docker ps -a


# 进入后台运行的容器
sudo docker exec -it 容器ID /bin/bash

# 从容器中退出
exit
ctrl+q+p

docker rmi 镜像ID
docker rm 容器ID

# -v 将主机的/home/tanght/haha目录 与 容器的/test目录 建立共享文件夹
# 主机目录要有写权限（最好放到自己的目录下，不要放到根目录，因为根目录可能没有写权限）
# 若主机目录没有写权限，则报错 xxxxx read only！
docker run -it -v /home/tanght/haha:/test /bin/bash 镜像ID

# 重命名容器  old_name可以在docker ps -a中查看
docker rename old_name new_name

# 从镜像创建容器  docker run == create + start
docker create [OPTIONS --name abc等等] 容器ID [COMMAND] [ARG...]

# 查看容器的标准输出
docker logs 容器ID

# 查看容器内部运行的进程
docker top
```

# Dockerfile

官方文档https://docs.docker.com/engine/reference/builder/

Dockerfile文件的名字必须是Dockerfile，格式如下

```dockerfile
# 指明构建的新镜像是来自于 centos:7 基础镜像
# FROM centos:7
# FROM centos   # 不写tag的话默认是:latest
FROM centos:latest

# 通过镜像标签声明作者信息
LABEL maintainer="son of bitch"

# 设置容器中的基础路径，影响COPY，ADD等涉及到容器中路径的命令
WORKDIR /usr/local

# 创建镜像层，多条命令用 && 连接，长度太长了用 \ 换行，可以执行任何shell命令
# 如果你愿意，甚至可以写篇小说
# 一般用于创建基本目录，安装基础软件
RUN mkdir -p /usr/local/mydir1 && mkdir -p /usr/local/mydir2 \
&& mkdir -p /usr/local/mydir3 && mkdir -p /usr/local/mydir4 \
&& echo "hahahahahahahahahahaha" && ping www.baidu.com \
&& curl http://www.baidu.com && yum -y install tree \
&& wget http://www.baidu.com && pip install django

# 将宿主机文件拷贝到镜像中并解压
# 拷贝 /build上下文/abc.tar.gz 至容器中 /WORKDIR/haha/xixi/ 并解压
ADD abc.tar.gz haha/xixi

# 将宿主机文件拷贝到镜像中，不解压
# 拷贝 /build上下文/abc.tar.gz 至容器中 /WORKDIR/haha/hehe/
COPY abc.tar.gz haha/hehe

# 暴露容器的8080端口给外部
# docker run -P (大写P) 自动端口映射的时候有用
# 也起到了提示的作用，告诉用户，这个docker的8080端口可以提供服务
EXPOSE 8080

# 设置容器内的环境变量
ENV JAVA_HOME /usr/local/java/jdk-11.0.6/
ENV PATH $PATH:$JAVA_HOME/bin

# 设置默认启动命令
# docker run imageid your_cmd 如果docker run时用户指定了命令，则dockerfile不需要ENTRYPOINT或者CMD
# docker run imageid 如果启动容器时用户没有指定特定的命令，则容器会运行ENTRYPOINT或CMD中设置的命令
# 如果docker run的时候用户没指定命令，且dockerfile中没写ENTRYPOINT或CMD，则容器启动失败
# 如果docker run时指定了命令，则以docker run时指定的命令为准
# ENTRYPOINT 不会被覆盖
ENTRYPOINT ["/bin/bash", "-c", "echo 'hello world'"]
```

指定build上下文

`docker build -t MyImages:v1 /home/tanght`这条命令的`/home/tanght`的意思是：指定build的上下文为`/home/tanght`，影响COPY等涉及到宿主机路径的命令。

WORKDIR

指定容器中的基础路径，简单起见避免用相对路径。

ADD&COPY

将宿主机的文件拷贝到容器中，ADD会自动解压，COPY不解压。ADD&COPY只能获取到宿主机上下文的文件。

ENTRYPOINT

容器的启动命令，不会被docker run的指定命令覆盖，docker run后面的字符串，会被当作参数传给ENTRYPOINT

CMD

容器的默认启动命令，会被docker run的指定命令覆盖

# 容器导入/导出

容器导出：将运行中的（或已经停止了的）容器，导出为压缩包

```shell
docker export web01 > /home/centos7-web01.tar
```

容器导入

```shell
# 将指定容器打包
docker export 容器ID > /path/xxx.tar

# 将xxx.tar还原成镜像，镜像的名字叫test:latest（不管export的时候镜像叫什么，这里强制重命名了）
docker import /path/xxx.tar test:latest


# 将指定镜像打包，拿U盘拷走吧您内~
docker save 镜像ID > /path/xxx.tar
# 或者用 -o 代替 >
docker save 镜像ID -o /path/xxx.tar

# 设置镜像名和标签，不设置的话load的时候，这个镜像是没有名字和标签的，需要load之后再次执行tag
docker save 镜像ID -o /path/xxx.tar

# 加载xxx.tar这个包，还原为一个镜像，save之前这个镜像叫什么，load之后还叫什么，不能重命名
docker load < /path/xxx.tar
# 或者用 -i 代替 <
docker load -i /path/xxx.tar
```



# 配置文件位置

```
/etc/docker/daemon.json
```

# 网络

请问c1，c2，c3这三个容器之间能通信么？互相能ping通么？

```shell
docker run --name c1 imageid
docker run --name c2 imageid
docker run --name c3 imageid
```

显然是不能的，因为每个容器都有自己的一套与**外界隔离**的网络环境，既与宿主机隔离，又与其它容器隔离。

如果要让c1，c2，c3之间通信，需要创建network，如下。

如果容器已经运行了

```shell
# 创建一个网络环境
docker network create my_test_network
# 将c1容器添加到这个网络中
docker network connect my_test_network c1
# 将c2容器添加到这个网络中
docker network connect my_test_network c2
# 将c3容器添加到这个网络中
docker network connect my_test_network c3
```

如果容器还未运行

```shell
docker network create my_test_network
# 启动时通过--network指定网络环境
docker run --name c1 --network=my_test_network imageid
docker run --name c2 --network=my_test_network imageid
docker run --name c3 --network=my_test_network imageid
```

## 相关命令

```shell
# 显示所有网络环境
docker network ls

# 查看netname网络的详细信息
docker network inspect netname

# 创建名字为netname的网络环境
docker network create netname

# 将容器添加到netname这个网络环境中
docker network connect netname container_name_or_container_id
```

## 四种网络模式

**host：**容器的网络环境不会与宿主机隔离，完完全全的使用宿主机的网络，容器中程序占用的端口会直接占用宿主机的端口，docker run的时候不需要-p作端口映射。容器中的localhost（或127.0.0.1）指向的是宿主机。`docker run --net=host`

**bridge：**容器有自己的虚拟网络，容器中的localhost（或127.0.0.1）指的是容器自己而不是宿主机。不用设置`--net=bridge`，因为这是默认的设置。

**none：**容器没有网络，此时的容器无法与外界有网络交互。`docker run --net=none`

**container：**附加到已存在的容器的网络环境中，多个容器使用同一个网络（与宿主机隔离）。

**共享网络环境（使用同一个网络环境）的意思：**例如A、B、C三个容器共享网络环境，A容器中的软件占用了80端口，B和C的软件就不能占用80端口了，B和C想访问80端口的话，直接localhost:80就行了，或者127.0.0.1:80。

## 容器host文件

#### 修改容器内的host文件的方法

##### 进入容器用vim修改，太麻烦

##### docker run的时候修改host文件的内容

`docker run --add-host=a.b.com:1.1.1.1 --add-host=c.d.com:2.2.2.2 ......`

##### 编写docker-compose.yml的时候指定

```yaml
services:
  service-nginx:
    image: nginx
    extra_hosts:
 	  - "a.b.com:1.1.1.1"
 	  - "c.d.com:2.2.2.2"
```


## 容器与宿主机通信

Q：一台电脑上面运行着一个容器，容器中运行着一个程序A。同时这台电脑上还运行这一个程序B，端口为8888。请问容器中的程序A如何访问宿主机上的程序B？

A：桥接模式下

## 容器之间通信

Q：一台电脑上面运行着2个容器A和B，A容器端口映射8888:8888，B容器端口映射9999:9999。请问容器A中的程序如何访问容器B的9999端口？

A：A中的程序直接访问`localhost:9999`是不行的，因为localhost指向的A自己，容器A和B的网络环境是完全隔离的。



# 常用脚本

运行一个nginx

```shell
sudo docker run --name test-nginx -d -p 9876:80 nginx:latest
```

