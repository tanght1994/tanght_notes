# SHELL快捷键

| 命令            | 作用                                    |
| --------------- | --------------------------------------- |
| Ctrl + U        | 清空命令行 （所有内容）                 |
| Ctrl + K        | 清空命令行 （当前光标位置以后所有内容） |
| Ctrl + W        | 清空命令行 （ 当前光标位置之前的单词）  |
| Ctrl + Y        | 粘贴Ctrl + [U,K,W]删除的内容            |
|                 |                                         |
| Ctrl + A        | 跳到命令行头部                          |
| Ctrl + E        | 跳到命令行尾部                          |
|                 |                                         |
| Ctrl + Z        | 暂停当前任务，并给出任务号[task_num]    |
| `bg [task_num]` | 去后台运行[task_num]这个任务            |
| `fg [task_num]` | 去前台运行[task_num]这个任务            |
|                 |                                         |
| Ctrl + D        | 关闭当前终端                            |
| Ctrl + L        | 清屏                                    |
|                 |                                         |

# 基本命令

## 创建新用户

```shell
# 切换为root用户
su root

# 创建tanght用户
useradd tanght

# 修改tanght用户的密码
passwd tanght
```



## 打包/压缩/解压

```shell
tar zxvf filename.tar
tar czvf filename.tar dirname

# 将所有.jpg文件，打包（不压缩）成haha.tar文件
tar -cf haha.tar *.jpg
# 将所有.gif文件，添加到haha.tar文件中
tar -rf haha.tar *.gif
# 列出haha.tar中包含的所有文件
tar -tf haha.tar
# 解包haha.tar
tar -xf haha.tar

# 忽略某些文件夹
# dir1
#     test1
#          other
#          test2
#     other
# --exclude后面跟的是相对于dir1的相对路径
tar --exclude=test1/test2 dir1.tar.gz dir1
```

注意：f参数必须在所有参数之后



## 软连接

```shell
# 在path2目录中创建一个path1文件(或者目录)的软链接
ln -s path1 path2
```



## 查看目录大小

```shell
du -sh
```





# 软件包安装



# 更换镜像源

## Centos

```bash
配置文件地址：/etc/yum.repos.d/CentOS-Base.repo
mv /etc/yum.repos.d/CentOS-Base.repo /etc/yum.repos.d/CentOS-Base.repo.backup # 备份
wget -O /etc/yum.repos.d/CentOS-Base.repo http://mirrors.aliyun.com/repo/Centos-5.repo # 下载新文件
wget -O /etc/yum.repos.d/CentOS-Base.repo http://mirrors.aliyun.com/repo/Centos-6.repo
wget -O /etc/yum.repos.d/CentOS-Base.repo http://mirrors.aliyun.com/repo/Centos-7.repo
```



## Ubuntu

```shell
pass
```





```shell
# 在~/目录下生成一个/mnt/hgfs/abc的软连接，名字为abc
ln  -s   /mnt/hgfs/abc   ~/

# 在/目录下查找名字为tanght的普通文件
find / -name tanght -type f











pass
```



# 定时任务

简述：crond为定时任务后台服务，为Linux提供定时任务功能，基本上任何一个Linux发行版都带有crond这个服务。crontab为crond的对外接口，使用户可以配置crond。

设置定时任务：在命令行中输入crond -e后，会打开一个虚拟文件，直接编辑这个文件就能实现定时任务的设置。文件中的每一行为一个定时任务，每行的的格式如下：

```shell
分  时  日  月  周  shell命令
```

可以运行shell命令就十分灵活了，因为可以用shell命令来运行我们自己编写的脚本或程序，如下：

```shell
# 每分钟运行ls命令，当然了crond是在后台运行我们的任务，所以ls的结果我们当然看不到了
* * * * * ls

# 每分钟运行  ls > /home/tanght/test.txt   这个命令，我们将ls的结果重定向到了test.txt中，这样我们就能看到结果了
* * * * * ls > /home/tanght/test.txt

# 每分钟运行   python3  /home/ubuntu/timedtasks/helloworld.py  my_arg   这个命令
# helloworld.py是我自己写的python脚本，接收1个参数
* * * * * python3 /home/ubuntu/timedtasks/helloworld.py 101.txt
```

使用方法

```shell
crond -e

# 以当前用户的身份设置定时任务，只能看到/编辑当前用户的定时任务
crond -e

# 以root用户来设置定时任务，能看到/编辑所有用户的定时任务
sudo crond -e
```

注意事项：

- 首次运行crond -e可能需要选择编辑器，选择vim就行了
- select-editor命令用来切换编辑器

## crontab时区

crontab的时区在`/etc/crontab`这个文件中设置，添加`CRON_TZ=Asia/Shanghai`这样一句配置的话，就是告诉crontab使用北京时间，修改了配置文件之后记得重启`sudo service crond restart`

使用service或者systemctl控制crontab的时候注意，这个程序有时候叫做crond有时候叫做cron，有可能跟系统版本有关



# Linux时区

## 查看时区

`date -R`可以查看当前的时区是什么，命令的结果是`Fri, 08 Jan 2021 15:54:32 +0800`，明显看到是`+0800`时区

## 修改时区

- 由`/etc/localtime`指向的文件决定，为什么说指向？因为localtime文件是个软连接，比如我的这台电脑是`/etc/localtime -> /usr/share/zoneinfo/Asia/Shanghai`，则这台电脑的时区就是北京时间。想要修改时区的话，直接改变`/etc/localtime`这个软连接的指向就好了，将它指向你想要的时区文件。时区文件在哪里？全部都在`/usr/share/zoneinfo/`这个文件夹下哦，自己去找吧
- `tzselect`命令可以告诉你时区文件的名字，是一个交互式的程序，按照程序的提示一步步选择就好了，结束之后`tzselect`会告诉你你想要的时区的时区文件名字是什么





# service命令

## 介绍

service程序是Linux的服务管理程序，可以方便的管理一些服务的启动/停止/重启等等

`service nginx start`这条命令的执行过程

- `sevice`程序去`/etc/init.d/`下寻找名字为`nginx`的shell脚本，注意脚本必须具有可执行权限
- `start`这个字符串作为第一个参数传递给这个脚本，并执行这个脚本
- 后面的事情就交给名字为nginx的这个脚本去做了

## 自定义service命令

- 编写脚本mytest
- 赋予mytest可执行权限`chmod 777 mytest`
- 将mytest放入`/etc/init.d/`目录下
- `service mytest`运行mytest，没有参数
- `service mytest arg1`运行mytest，传入一个参数，脚本中可以通过`$1`获取
- `service mytest arg1 arg2 arg3`运行mytest，传入三个参数，脚本中通过`$1 $2 $3`获取



```shell
sudo service --status-all
 [ - ]  acpid
 [ + ]  apparmor
 ......
 [ + ]  atd
 [ - ]  console-setup.sh
 [ + ]  cron
```





# systemctl

查看service源码可知，对于标准命令如start，stop，restart等，即使使用`service name start`去操作，但是后台也偷偷将service换成了systemctl。

```shell
# 这两个命令是一样的
service cron start
systemctl start cron
```

```shell
systemctl list-unit-files --type=service   # 列出所有服务（包括启用的和禁用的）
systemctl list-units --all --state=inactive # 列出所有没有运行的 Unit
systemctl list-units # 列出正在运行的 Unit
systemctl list-units --all # 列出所有Unit，包括没有找到配置文件的或者启动失败的
systemctl list-units --failed # 列出所有加载失败的 Unit


systemctl status mysql # 查看mysql服务的状态，详细信息中会写着管理mysql服务的service脚本在哪里
```

## 命令1

```shell
systemctl list-unit-files --type=service   # 列出所有服务（包括启用的和禁用的）
systemctl list-units --all --state=inactive # 列出所有没有运行的 Unit
systemctl list-units # 列出正在运行的 Unit
systemctl list-units --all # 列出所有Unit，包括没有找到配置文件的或者启动失败的
systemctl list-units --failed # 列出所有加载失败的 Unit
```



## 命令2

```shell
systemctl status mysql # 查看mysql服务的状态，详细信息中会写着管理mysql服务的service脚本在哪里
systemctl stop mysql # 停止
systemctl restart mysql # 重启mysql
systemctl enable mysql # 设置开机启动(在/etc/systemd/system/下创建一个软连接指向/lib/systemd/system/)
systemctl disable mysql # 取消开机启动
systemctl is-enabled mysql # 查看是否是开机启动
```





| Unit            |                                   |                                                              |
| --------------- | --------------------------------- | ------------------------------------------------------------ |
| After           | 表示服务需要在***服务启动之后执行 | 无依赖                                                       |
| Before          | 表示服务需要在***服务启动之前执行 | 无依赖                                                       |
| Wants           | 弱依赖关系                        |                                                              |
| Requires        | 强依赖关系                        | ***停止之后本服务也必须停止                                  |
| Service         |                                   |                                                              |
| EnvironmentFile | 环境参数文件                      | EnvironmentFile=/etc/sysconfig/sshd以key=value的形式保存以$key形式读取 |
| ExecStart       | 启动进程时执行的命令              |                                                              |
| ExecReload      | 重启服务时执行的命令              |                                                              |
| ExecStop        | 停止服务时执行的命令              |                                                              |
| ExecStartPre    | 启动服务之前执行的命令            |                                                              |
| ExecStartPost   | 启动服务之后执行的命令            |                                                              |
| ExecStopPost    | 停止服务之后执行的命令            |                                                              |



/etc/systemd/system/这个目录好像是开机启动的，里面的文件大多是指向/lib/systemd/system/目录下的service文件

/lib/systemd/system/这个目录保存了所有.service文件



## service文件

[Unit]
After=network.target
\#[Service]部分是服务的关键，是服务的一些具体运行参数的设置，这里Type=forking
\#是后台运行的形式，PIDFile为存放PID的文件路径，ExecStart为服务的具体运行命令，
\#ExecReload为重启命令，ExecStop为停止命令，PrivateTmp=True表示给服务分配独
\#立的临时空间，注意：[Service]部分的启动、重启、停止命令全部要求使用绝对路径，使
\#用相对路径则会报错！
[Service]
Type=forking
PIDFile=/home/developer/web/gunicorn.pid
ExecStart=/usr/local/bin/forever start 
ExecReload=/bin/kill -s HUP $MAINPID
ExecStop=/bin/kill -s QUIT $MAINPID
PrivateTmp=true
\#[Install]部分是服务安装的相关设置，可设置为多用户的
[Install]
WantedBy=multi-user.target



man systemd.unit  service文件的帮助文档





所有的启动设置之前，都可以加上一个连词号（-），表示"抑制错误"，即发生错误的时候，不影响其他命令的执行。比如，EnvironmentFile=-/etc/sysconfig/sshd（注意等号后面的那个连词号），就表示即使/etc/sysconfig/sshd文件不存在，也不会抛出错误。



修改配置文件以后，需要重新加载配置文件，然后重新启动相关服务。

重新加载配置文件

systemctl daemon-reload



# 后台运行

`command`：前台运行command。stdout与stderr都直接输出到当前窗口

`command >/dev/null`：stderr直接输出到当前窗口，stdout输出到黑洞

`command >/dev/null 2>&1`：2>&1的意思是stderr输出到stdout，也就是说stderr也去黑洞了

`command >/dev/null 2>&1 &`：&的意思是后台运行程序，也就是说从当前窗口不能给此程序发送信号了，不能给此程序标准输入了

`nohup command >/dev/null 2>&1 &`：nohup的意思是告诉此程序不要处理SIGHUP信号，什么时候会有SIGHUP信号呢？关闭当前窗口时，当前窗口会给此窗口下的所有程序发送SIGHUP信号

## &

在任何命令后面加上&，就会将此命令/程序放到后台运行。

后台运行意味着什么呢？意味着不能从当前终端给这个程序标准输入了，所以我们能看到，后台运行的程序不会阻塞住当前终端，当前终端可以立即接受新的用户操作；意味着不能从当前终端给程序传递信号了，Ctrl+C不管用了；

## nohup

在一条命令/程序之前加上nohup，就会使此程序忽略SIGHUP信号

SIGHUP信号是什么鬼？当关闭某个终端时，这个终端会给自己下面的所有程序发送SIGHUP信号，通知自己的程序"我死了，你们看着办吧"，程序在收到这个信号时就会知道终端死了，就可以决定自己下一步该怎么办，大部分程序的行为都是跟着终端一起去死。

## 2>&1

任何命令后方加上2>&1，就会将此程序的stderr重定向到stdout

stderr重定向到stdout？我没听错吧？这什么意思？意思就是，stdout去哪里，我stderr就去哪里，我跟定你了！

`command > 123.txt`这个命令只是将stdout重定向到123.txt了，stderr依然向终端喷射东西，所以加上2>&1会将stderr也扔到123.txt，当然了，也可以直接使用2>123.txt，这样的话就需要打开两次123.txt,而且stdout与stderr的输出可能会相互覆盖



# SSH登陆

电脑A通过第三方工具远程控制电脑B，电脑A每次控制电脑B时都需要输入密码，为了避免重复输入密码，可以使用SSH服务，将电脑A的公钥放入电脑B的SSH的authorized_keys中。

在该用户家目录的.ssh文件夹下找到authorized_keys这个文件(没有就新建)，确认这个文件的权限是600(不是的话就改成600)，将另一台电脑生成的公钥复制到authorized_keys这个文件中，保存，重启ssh服务。

允许root使用ssh登陆，需要修改/etc/ssh/sshd_config文件，添加一句命令`PermitRootLogin yes`

出现警告`the ECDSA host key for 'xxxx' differs from the key for the IP address 'xxxxx'`，删除电脑A的known_hosts文件，这个文件在该用户家目录的.ssh文件夹中



# 动态库路径

`export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:your_path`

Linux中的动态加载器通过ld.so.cache文件决定搜索动态库的路径

ld.so.cache通过ld.so.conf生成，使用ldconfig命令

ld.so.conf中一般是`include /etc/ld.so.conf.d/*.conf`，意思是包含ld.so.conf.d中的.conf文件

所以用户可以在ld.so.conf.d中新增自己的.conf文件，将路径写到自己的文件中就行了



# g++ include路径

查看

g++ -v -E -x c++ -

CPATH环境变量影响gcc与g++的include

CPLUS_INCLUDE_PATH影响g++

C_INCLUDE_PATH影响gcc



# source命令

```shell
source test.sh		# 将test.sh中的代码读出来，放到本窗口的命令行中执行(本shell直接运行test.sh中的命令)
. test.sh			# . 同 source
./test.sh			# 启动子进程，运行test.sh脚本
sh test.sh			# sh 同 ./
```

例子：

export的环境变量对本shell以及本shell的子程序起作用。如果定义了一个环境变量但是不export，则此环境变量只对本shell起作用，对它的子程序不起作用。所以如果我们编写了一个脚本如下：

```shell
# export_env.sh
# 此脚本的作用就是定义几个环境变量给gcc使用
export LD_LIBRARY_PATH=/home/tanght/download/boost_1_75_0/stage/lib:${LD_LIBRARY_PATH}
export LIBRARY_PATH=/home/tanght/download/boost_1_75_0/stage/lib:${LIBRARY_PATH}
export CPATH=/home/tanght/download/boost_1_75_0:${CPATH}
```

如果我们`./export_env.sh`这样运行这个脚本，则会发现`echo ${CPATH}`并没有按照我们的想法被设置，跟我们没有运行这个脚本之前是一样的。

那是因为export_env.sh这个脚本是以一个子进程的形式运行的，子进程中设置的环境变量并不能传递给它的父进程(也就是我们的操作窗口)。

所以如果想要在本窗口中设置环境变量，只能将上面的代码复制到命令行中执行一下了。。。哈哈，那样岂不是太弱了，一点逼格都没有！牛逼的方法看下面！

source命令的作用是什么呢？`source export_env.sh`这个命令的意思是：别用子进程运行export_env.sh这个脚本，直接将export_env.sh这个文件中的命令读出来，直接在本窗口中运行！

# 防火墙

## centos7

```shell
systemctl status/start/stop firewalld
```

## centos6

```
service iptables status/start/stop
```

