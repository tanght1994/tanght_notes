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
	"registry-mirrors":["https://mirror.ccs.tencentyun.com"]
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

又比如nginx的基础镜像，第一条命令是以守护进程的模式启动nginx（后台运行），那么当PID为1的进程结束的时候，容器马上就结束了，所以nginx要以前台模式运行在容器中。

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
# 根据 imageID 这个镜像，创建一个新容器，并运行容器
# -it提供交互终端
# -p 8000:80  将主机的8000端口映射到容器的80端口
docker run --name haha -p 8000:80 -it imageID command

# --name tht_nginx    docker ps的时候会显示tht_nginx这个名字用以提示
# -p 8080:80    将主机的8080端口映射到本容器的80端口（主机的8080端口与容器的80端口绑定到一起了，成为一体了）
# -d 容器以后台程序运行，不提供交互终端
docker run --name tht_nginx -p 8080:80 -d f35646e83998

# xxx --
docker run -d ubuntu sleep infinity
```

## 退出容器

```python
# 从容器中退出，如果
exit

# 从容器中退出，并且继续保持容器运行
ctrl+q+p
```

## 进入容器

```python
# 进入后台运行的容器
sudo docker exec -it 容器ID /bin/bash
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

构建镜像的命令为：`docker build -t xxx:v1 .`

构建 docker 镜像有两种方式：

1. **非dockerfile**
   1. run一个基础镜像
   2. 在这个容器中用 linux 命令来配置这个容器中的环境，比如 apt install 等等
   3. 将这个容器导出为镜像
   4. 然后就可以run这个新镜像了

2. **使用dockerfile**

   1. 将配置环境的 linux 命令写在dockerfile中

   2. 使用 `docker build -t xxx:v1 .` 生成镜像
   3. 然后就可以run这个新镜像了

Dockerfile文件的名字必须是Dockerfile，格式如下：

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

## ENTRYPOINT与CMD

- ENTRYPOINT是主命令
- CMD是ENTRYPOINT的默认参数，可以没有CMD，这就意味着ENTRYPOINT不需要参数
- docker run时传递的参数会覆盖CMD然后追加到ENTRYPOINT的参数中

```dockerfile
# dockerfile
FROM ubuntu
# 设置默认的入口点命令
# 主命令，无法被覆盖，谁来了都不能把他覆盖
ENTRYPOINT ["echo"]
# 设置默认参数
CMD ["Hello, World!"]
```

`docker run dockername`：容器的启动命令为`echo "Hello, World!"`

`docker run dockername Hi`：容器的启动命令为`echo Hi`

总结：

- 正经的容器都是首先设置ENTRYPOINT，然后用CMD给ENTRYPOINT传递默认参数。
- 如果用户在docker run的时候没有传递参数（没有覆盖cmd），则ENTRYPOINT使用dockerfile中cmd设置的参数。
- 如果用户不满意默认的cmd参数，在docker run的时候传递了参数，则会优先使用用户传递的参数给ENTRYPOINT。
- 如果用户在docker run的时候不满意ENTRYPOINT，则可通过----entrypoint来修改ENTRYPOINT（强烈不建议）

## 命令的两种格式

加不加[]（中括号）的区别

### shell格式（无[]）

与在linux的cmd中执行命令是一样的，主进程是/bin/sh，由/bin/sh的子进程去执行用户的命令

```dockerfile
CMD ping www.baidu.com
```

实际执行的命令是`/bin/sh -c 'ping www.baidu.com'`

所以容器内的1号进程是`/bin/sh`，`/bin/sh`fork子进程来执行`ping`命令，给容器发送信号会发送给`/bin/sh`

1. 首先找到`/bin/sh`程序，如果容器内没有`/bin/sh`程序则启动失败
2. 然后寻找`ping`程序，如果ping不在`path`环境变量中，则启动失败
3. 然后`sh`程序fork一个子进程来执行`ping www.baidu.com`

### exec格式（有[]）

直接执行可执行程序，不需要借助/bin/sh

```dockerfile
CMD ["/bin/ping", "www.baidu.com"]
```

实际执行的命令是`/bin/ping www.baidu.com`

所以容器内的1号进程是`/bin/ping`，，给容器发送信号会发送给`/bin/ping`

1. 首先找到`/bin/ping`程序，这是绝对路径，所以不依赖`path`环境变量
2. 然后直接执行`/bin/ping www.baidu.com`

### 总结

exec格式要优于shell格式，因为exec格式的依赖比较少，即使容器内没有`/bin/sh`程序也能运行

请永远使用exec格式，shell格式会出现你意想不到的结果

## 构建时mount

mount可以在构建过程中将宿主机的目录（甚至是远程的某个镜像中的目录）挂载到当前正在构建的docker中，构建结束后，解除挂载。

下面的代码的作用是：先将远程镜像（from=infiniflow/ragflow_deps:latest）的（source=/huggingface.co）这个目录挂载到当前docker的（target=/huggingface.co）这个目录下，然后将（/huggingface.co/InfiniFlow/huqie/huqie.txt.trie）这个文件复制到当前容器的（/ragflow/rag/res/）目录下。

```dockerfile
RUN --mount=type=bind,from=infiniflow/ragflow_deps:latest,source=/huggingface.co,target=/huggingface.co
RUN cp /huggingface.co/InfiniFlow/huqie/huqie.txt.trie /ragflow/rag/res/
```

## 继承基础镜像

```dockerfile
# 继承基础镜像
FROM centos:latest

# 一些自定义的操作...

# 覆盖基础镜像的启动命令, 如果想使用基础镜像的 ENTRYPOINT, 那这里就不要定义 ENTRYPOINT
ENTRYPOINT ["/bin/bash", "-c", "echo 'hello world'"]
```

## 查看镜像的ENTRYPOINT

```shell
# 这个命令会显示镜像的很多信息，ENTRYPOINT就在其中
docker inspect 镜像名称或ID
```

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
docker save 镜像名:版本 -o /path/xxx.tar

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

## 简介

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
# 创建一个网络环境, 名字是my_test_network
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

这样c1，c2，c3之间就能互相ping通了，**直接ping容器名称**（--name后面指定的名称）就行

```shell
# 进入容器c1
docker exec -it c1 /bin/sh
# 在 c1 中 ping c2
ping c2
# 在 c1 中 ping c3
ping c3
```

docker compose 中设置网络

```yaml
version: '3.3'
services:
  haha1:
    image: nginx
    ports:
      - 11001:80
    networks:
    - tanghtnetwork1  # 加入 tanghtnetwork1 这个网络

  haha2:
    image: nginx
    ports:
      - 11002:80
    networks:
    - tanghtnetwork1  # 加入 tanghtnetwork1 这个网络

networks:
  tanghtnetwork1:  #  创建网络环境 tanghtnetwork1
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

# docker-compose

同一台物理机上运行多个docker，使用docker-compose来进行管理会非常方便

多个物理机上运行多个docker，使用k8s

- docker服务名：用于同一个docker网络中，不同docker间的通信
- docker容器名：用于操作docker

## 例子

```yaml
services:
  es01: # docker服务名称，用于同一个docker网络中，不同docker间的通信，http://es01:8080就能访问这个docker的8080端口
    container_name: ragflow-es-01 # docker容器名
    profiles: # 给容器添加标签，docker-compose --profile x up, 只启动拥有x标签的容器
      - elasticsearch
    image: elasticsearch:1.0.0
    volumes:
      - esdata01:/usr/share/elasticsearch/data # 将宿主机目录与容器内目录进行绑定
    ports:
      - 9200:9200 # 将宿主机端口与容器内端口进行绑定
    env_file: .env # 环境变量 优先级低于 environment
    environment: # 环境变量 优先级高于 env_file
      - node.name=es01
      - ELASTIC_PASSWORD=xxxxx
      - bootstrap.memory_lock=false
      - discovery.type=single-node
      - xpack.security.enabled=true
      - xpack.security.http.ssl.enabled=false
      - xpack.security.transport.ssl.enabled=false
      - cluster.routing.allocation.disk.watermark.low=5gb
      - cluster.routing.allocation.disk.watermark.high=3gb
      - cluster.routing.allocation.disk.watermark.flood_stage=2gb
      - TZ=xxx
    mem_limit: 100000000 # 容器能使用的最大内存
    ulimits: # linux的ulimit配置
      memlock:
        soft: -1
        hard: -1
    healthcheck: # 健康检查，docker管理程序通过这个命令来判断此容器是否健康，不健康就重启
      test: ["CMD-SHELL", "curl http://localhost:9200"]
      interval: 10s
      timeout: 10s
      retries: 120
    networks:
      - ragflow # 使用名字为ragflow的网络
    restart: on-failure

  mysql:
    image: mysql:8.0.39
    container_name: ragflow-mysql
    env_file: .env
    environment:
      - MYSQL_ROOT_PASSWORD=xxxx
      - TZ=xxxx
    command: # 覆盖默认的CMD
      --max_connections=1000
      --character-set-server=utf8mb4
      --collation-server=utf8mb4_unicode_ci
      --default-authentication-plugin=mysql_native_password
      --tls_version="TLSv1.2,TLSv1.3"
      --init-file /data/application/init.sql
    ports:
      - 3306:3306
    volumes:
      - mysql_data:/var/lib/mysql
      - ./init.sql:/data/application/init.sql
    networks:
      - ragflow
    healthcheck:
      test: ["CMD", "mysqladmin" ,"ping", "-uroot", "-p${MYSQL_PASSWORD}"]
      interval: 10s
      timeout: 10s
      retries: 3
    restart: on-failure

  redis:
    image: valkey/valkey:8
    container_name: ragflow-redis
    command: redis-server --requirepass xxx --maxmemory 128mb --maxmemory-policy allkeys-lru
    env_file: .env
    ports:
      - 6379:6379
    volumes:
      - redis_data:/data
    networks:
      - ragflow
    restart: on-failure

volumes:
  esdata01:
    driver: local
  mysql_data:
    driver: local
  redis_data:
    driver: local

networks:
  ragflow: # 定义一个网络，同一个网络中的docker容器可以相互访问
    driver: bridge
```

## 命令

```shell
# -f 用于指定配置文件 不指定的话 默认是当前目录下的docker-compose.yml
# -d 让 docker-compose 后台运行，否则 docker-compose 会占用当前终端
# -p 设置项目名, 默认是当前文件夹的名字为项目名
docker-compose -f xxx.yml -p abc up -d

# 停止并清理被此配置文件所管理的资源(停止容器、删除容器、删除网络等)
docker-compose -f xxx.yml down

# 进入容器中（也可以直接用docker命令进入）
docker-compose -f xxx.yml exec nginx bash

# 重启docker-compose.yml中包含的所有docker
docker-compose restart
```



环境变量

```yaml
  c1:
    image: centos
    container_name: c1
    environment:
      # k: v
      # v 会去除前后空格
      DOG: i am a dog
      cat:       i am a cat
      HAHA: xixixixi
    command: sleep 1d

  c2:
    image: centos
    container_name: c2
    environment:
      # k=v
      # v 不会去除前后空格
      - discovery.type=single-node
      - network.host=0.0.0.0
      - ES_JAVA_OPTS=-Xms128m -Xmx128m
    command: sleep 1d
```







yml

```yaml
version: '3.3'

# 创建网络环境
networks:
  tanghtnetwork1:       # 相当于docker命令行 docker network create tanghtnetwork1
    # ipam:             # 不用写这两行, 默认值就是创建bridge的网络
    #   driver: bridge  # 不用写这两行, 默认值就是创建bridge的网络
  tanghtnetwork2:       # 相当于docker命令行 docker network create tanghtnetwork2
    ipam:
      driver: host      # 可以在 ipam.driver 处设置网络类型 可选值为 host, bridge, container, none

services:
  haha1:                    # 创建 1 个容器
    image: centos
    restart: always
    privileged: true
    networks:
    - tanghtnetwork1
    command: sleep 60s
    container_name: haha1   # 相当于 docker 命令行的 --name haha1, 不指定容器名称的话则随即设置

  haha2:                    # 创建 1 个容器
    image: centos
    restart: always
    privileged: true
    networks:
    - tanghtnetwork1
    command: sleep 60s
    container_name: haha2

  haha3:                    # 创建 1 个容器
    image: centos
    restart: always
    privileged: true
    networks:
    - tanghtnetwork1
    command: sleep 60s
    container_name: haha3
```





# 装机必备

```yaml
version: '3.3'
services:
  redis:
    image: redis:latest
    container_name: redis
    restart: always
    privileged: true
    ports:
      - 6379:6379
    environment:
      - TZ=Asia/Shanghai
    volumes:
      - /dockerstore/redis/data:/data
      - /dockerstore/redis/logs:/logs
    command:
      - --requirepass "Tht940415,./"

  mysql:
    image: mysql:latest
    container_name: mysql
    restart: always
    ports:
      - 3306:3306
    privileged: true
    volumes:
      - /dockerstore/mysql/var/lib/mysql:/var/lib/mysql
    environment:
      - MYSQL_ROOT_PASSWORD=Tht940415,./
    command:
      - --character-set-server=utf8mb4

  elasticsearch:
    image: elasticsearch:7.5.2
    container_name: elasticsearch
    restart: always
    volumes:
      - /dockerstore/elasticsearch/usr/share/elasticsearch/data:/usr/share/elasticsearch/data
    environment:
      - discovery.type=single-node  # 单节点启动
      - network.host=0.0.0.0  # 可外部访问, 否则只能本机访问
      - ES_JAVA_OPTS=-Xms128m -Xmx128m  # 限制es内存使用量最大128M
      - TAKE_FILE_OWNERSHIP=true  # 赋予volumes写权限, 不然es无法向挂载的目录中写入数据, 不知道es为什么这么蠢
    ports:
      - 9200:9200
      - 9300:9300
    privileged: true

  kibana:
    image: kibana:7.5.2
    container_name: kibana
    restart: always
    privileged: true
    environment:
      - ELASTICSEARCH_HOSTS=["http://elasticsearch:9200"]
      - SERVER_HOST=0.0.0.0
    depends_on:
      - elasticsearch
    ports:
      - 5601:5601

  prometheus:
    image: prom/prometheus:latest
    container_name: prometheus
    restart: always
    privileged: true
    volumes:
      - /dockerstore/prometheus/opt/bitnami/prometheus/data:/opt/bitnami/prometheus/data
    ports:
      - 9090:9090

  grafana:
    image: grafana/grafana:latest
    container_name: grafana
    restart: always
    privileged: true
    ports:
      - 3000:3000

```

# Windows端口占用

使用管理员cmd执行下列命令

winnat与docker有时候有冲突

```shell
net stop winnat
启动你的容器
net start winnat
```

