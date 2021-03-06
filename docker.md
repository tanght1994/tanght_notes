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
	"registry-mirrors":["https://reg-mirror.qiniu.com/"] # 加速地址是在阿里云上申请的
}
```

docker images







# 帮助文档

输出所有命令`docker --help`

```shell
docker --help
# 以下是输出
Usage:  docker [OPTIONS] COMMAND

Options:
      --config string      Location of client config files (default "/root/.docker")
  -D, --debug              Enable debug mode
  -v, --version            Print version information and quit
  ...

Management Commands:
  config      Manage Docker configs
  container   Manage containers
  volume      Manage volumes
  ...

Commands:
  commit      Create a new image from a container's changes
  cp          Copy files/folders between a container and the local filesystem
  create      Create a new container
  exec        Run a command in a running container
  images      List images
  ps          List containers
  restart     Restart one or more containers
  ...
```

查看某个命令的使用方法`docker xxx --help`

```shell
docker create --help
# 以下是输出
Usage:  docker create [OPTIONS] IMAGE [COMMAND] [ARG...]

Create a new container

Options:
      --add-host list                  Add a custom host-to-IP mapping (host:ip)
  -a, --attach list                    Attach to STDIN, STDOUT or STDERR
      --blkio-weight-device list       Block IO weight (relative device weight) (defa
      --name string                    Assign a name to the container
      --restart string                 Restart policy to apply when a container exits (default "no")
      --rm                             Automatically remove the container when it exits
  -t, --tty                            Allocate a pseudo-TTY
      --ulimit ulimit                  Ulimit options (default [])
  -u, --user string                    Username or UID (format: <name|uid>[:<group|gid>])
      --userns string                  User namespace to use
      --uts string                     UTS namespace to use
  -v, --volume list                    Bind mount a volume
  -w, --workdir string                 Working directory inside the container
  ...
```





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

# 加载xxx.tar这个包，还原为一个镜像，save之前这个镜像叫什么，load之后还叫什么，不能重命名
docker load < /path/xxx.tar
```





```
```

