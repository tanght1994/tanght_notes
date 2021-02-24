# 简介

uwsgi是一个用c语言写成的程序，这个程序的功能非常简单，就是监听一个端口，然后读取这个端口收到的字符串，再将这些字符串交给一个python函数来处理，最后将这个python函数的返回值返回给端口对面的机器。

这个python函数长什么样子呢？是一个接收两个参数，返回一个可迭代对象的函数，他的名字可以是django，flask等等。

django本质上是一个复杂的函数，接收两个参数，返回一个可迭代对象。

启动uwsgi，uwsgi创建一个python解释器，python解释器去加载django。然后uwsgi创建一个socket，开始监听这个端口，比如就是80端口。80端口收到消息，uwsgi将消息整理之后传递个django，django使用用户写的函数来处理消息，处理完毕后将结果返回给uwsgi，uwsgi对结果做简单的整理然后传递给80端口的对面机器。



# 简单服务器

前面说了，uwsgi程序只需要我们写一个application函数(名字必须为application)，接收两个参数，返回一个字符串(bytes类型，不能是str类型)，就这么简单，那么我们就写一个下面的函数，保存到haha.py中。

```python
# /home/tanght/haha.py
def application(env, start_response):
    start_response('200 OK', [('Content-Type','text/html')])
    return 'Hello World'.encode('utf-8')
```

ok，给uwsgi程序准备的函数写好了，那么现在我们可以启动uwsgi了。

```shell
uwsgi --http 0.0.0.0:8000 --wsgi-file tanght.py
```

输入上述命令，回车！搞定！可以看到命令行窗口中输出了一堆乱七八糟的信息，然后阻塞住不动了。这就证明uwsgi启动成功了，uwsgi作为一个程序，占用了当前的cmd窗口。

`--http 0.0.0.0:8000`是告诉uwsgi监听本机的8000端口。

`--wsgi-file`是告诉uwsgi我们的application函数所在的文件。

现在uwsgi就在循环监听8000端口了，只要8000端口来消息，uwsgi就会调用我们的application函数来处理，并且uwsgi会将application函数的返回值传递给对方。











# 命令

```python
# 直接将uwsgi需要的参数通过命令行传递个它，这样启动之后，uwsgi会占用当前shell窗口，就是所谓的前台运行，关了这个shell或者ctrl+c之后，uwsgi就停止了
uwsgi --http 0.0.0.0:8000 --wsgi-file myfile.py

# 通过配置文件给uwsgi传递参数
uwsgi --ini your_path/your_uwsgi_config_name.ini

# 优雅的停止
uwsgi --stop you_pid.pid

# 重新加载uwsgi.ini配置文件，重新加载django项目，django
uwsgi --reload you_pid.pid
```



# uwsgi.int

```python
# 这些参数既可以通过命令行传递，也可以通过这个配置文件来传递，一般都用配置文件，因为参数太多了
[uwsgi]

# 需要监听的端口号
# socket = 0.0.0.0:8000
http = 0.0.0.0:8000

# chdir设置当前工作目录，影响os.getcwd()，open(相对路径)
# 如果不设置chdir的话，在哪里运行的uwsgi命令，就将那个路径设置为当前工作目录
# 在app加载前切换到当前目录， 指定运行目录
# 这个变量会影响python导包的路径，因为uwsgi在启动python解释器的时候会将'.'放到sys.path中
chdir = /home/ubuntu/python/uwsgi_test/uwsgi1

# 虚拟环境不用设置，直接运行虚拟环境中uwsgi，则uwsgi将自动使用虚拟环境
# venv = /home/ubuntu/python/uwsgi_test/uwsgi1/.venv
# home = /home/ubuntu/python/uwsgi_test/uwsgi1/.venv
# uwsgi --help | grep vir

# 指定后台输出日志信息的文件
daemonize = /home/ubuntu/python/uwsgi_test/uwsgi1/log.log

# 指定运行时候的pid文件，也可以用来停止进程， uwsgi --stop /var/run/uwsgi_pid.log
pidfile = /home/ubuntu/python/uwsgi_test/uwsgi1/pid.log

# django项目同名目录内层自动生成的wsgi.py的路径，如果你的项目叫taobao，就填taobao.wsgi
# module = Blog.wsgi

# xxxxx
wsgi-file = /home/ubuntu/python/uwsgi_test/uwsgi1/test.py

# 开启主进程
master = true

# 最大进程数量
processes = 4

# uwsgi停止时，自动删除unix socket文件和pid文件
vacuum = true

# buffer-size = 32768

# python代码变动时自动重启
py-autoreload=1
```
