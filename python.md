# 想固定当前工作目录？

将以下代码放在main文件代码最前面，一定要最前面。这样不管在何处运行此程序，程序的cwd都会是main文件的所在目录。

```python
import os
# 获得当前文件的绝对路径（带文件名字）
abspath = os.path.abspath(__file__).replace('\\', '/')
# 删除文件名字
work_dir = abspath[0: abspath.rfind('/')]
# 设置程序的工作目录
os.chdir(work_dir)
```



# pylint恶心的红色下划线

**pylint忽略整个文件**

将下方代码放到此文件的第一行，pylint就不会检查这个文件了

```python
# pylint: skip-file
```

**pylint忽略某段代码**

先disable，再enable。处于disable与enable之间的代码，不会被检查。

例子：下方代码忽略E1101错误

```python
# pylint: disable=E1101
you code
...
...
# pylint: enable=E1101
```

例子：下方代码忽略 no-member 错误

```python
# pylint: disable=no-member
you code
...
...
# pylint: enable=no-member
```

E1101与no-member是相同的意思，写哪个都一样。

**查看错误编号，为什么是E1101？**

通过执行下方命令，可以查看具体的错误编号

```
pylint your.py
```



```python
__init__.py中的__path__
# 只有__init__.py文件中才有__path__变量，__path__[0]为这个包的绝对路径
```



# 动态导入函数(或者类)

自己写了一个包，名字为mymodel，包中带有一个class Test，我们在其他文件中导入Test类（Test是类也行，是函数也行，都一样），有两种方法，如下：

第一种，简单直观，不支持动态变化

```python
# 导入mymodel中的Test类
from mymodel import Test

# 实例化Test类生成一个test对象
test = Test()
```

第二种，变态写法，不直观，无法智能补全，但是装逼满分，且支持动态变化

```python
# 导入mymodel包
import mymodel

# 从mymodel中获取名字为Test的东西(我们这里当然是类喽~，python并不关心Test到底是什么，类也行，函数也行，变量也行，什么都可以)，并且用classModel来表示它
classModel = getattr(mymodel, 'Test')

# 实例化classModel(不要忘了classModel其实是mymodel中的Test哦，其实是实例化我们的Test类)
test = classModel()
```

什么是动态变化？

比如说我的mymodel中有Test1、Test2、，，，Test10这10个类，但是其他文件会根据情况有选择的来导入某一个，怎么办？

```python

import mymodel

# 根据情况选择性的给s赋值
s = 'Test10'
if xxx:
	s = 'Test1'
elif xxx:
    s = 'Test2'
elif xxx:
    s = 'Test3'
elif xxx:
    s = 'Test4'
    .
    .
    .
# 从mymodel中导入
classModel = getattr(mymodel, s)
test = classModel()
```



# import_module

```python
# 装逼神器，装逼者必备技能，保证写出来的代码没几个人能看懂，时间长了自己都看不懂
from importlib import import_module
# 从sys.path路径下寻找tanght文件夹(文件夹下必须带__init__.py，否则python不认为这个文件夹是包)并加载
m = import_module('tanght')

# 加载[sys.path]/zhangsan/lisi/wangwu这个路径下的haha
# 如果haha是个文件，则加载haha.py，如果没有haha.py则报错
# 如果haha是个目录，则加载haha目录下的__init__.py文件，如果没有__init__.py文件则报错
m = import_module('zhangsan.lisi.wangwu.haha')
```









# 虚拟环境

python程序由两个exe文件组成：

1. python.exe：python解释器
2. pip.exe：这个python.exe的安装包助手，此pip.exe终身绑定此python，pip.exe编译的时候就硬编码绑定的，无法修改。pip --version命令可以查看此pip帮的python解释器是哪个。
3. 进入到pip.exe的目录中执行pip install命令，这个命令安装的包裹是给对应的python使用的，多个版本的python不会混乱。
4. python -m pip install，使用此python绑定的pip执行install命令。

例子：

windows电脑中存在两个python版本，且没有设置PATH环境变量，如下：

- python3.7的python可执行文件位置 D:/python/python37/python.exe
- python3.7的pip可执行文件位置 D:/python/python37/Scripts/pip.exe
- python3.8的python可执行文件位置 D:/python/python38/python.exe
- python3.8的pip可执行文件位置 D:/python/python38/Scripts/pip.exe

在D:/python/python37/目录下执行python命令，这时会启动D:/python/python37/python.exe这个软件
在D:/python/python37/Scripts/目录下执行pip install命令，这时会将包裹安装到D:/python/python37/下的某个目录中
D:/python/python37/Scripts/pip.exe与D:/python/python37/python.exe是绑定的

## venv

```shell
# 在当前目录下创建python虚拟环境，命名为.venv
python3 -m venv .venv

# 进入虚拟环境
source .venv/bin/activate

# 离开虚拟环境
deactivate

# windows中进入虚拟环境的方法
.venv\Scripts\activate.bat

# windows中离开虚拟环境的方法
直接关闭cmd窗口就行了
```

## pipenv

```shell
# 在当前目录创建指定python版本的虚拟环境
pipenv --python "your_python_path/python.exe"

# 根据当前目录下的 Pipfile 安装所有已声明的依赖包。如果没有虚拟环境，会自动创建
# 相当于 npm install
pipenv install

# 安装指定的包，并自动添加到 Pipfile 的 [packages] 区块中
pipenv install <包名>

# 安装指定的包作为开发依赖，并记录到 Pipfile 的 [dev-packages] 区块中
pipenv install --dev <包名>

# 卸载指定包，并自动更新 Pipfile（移除该包的依赖声明）
pipenv uninstall <包名>

# 启动 pipenv 创建的虚拟环境，即进入该环境的交互式 shell
pipenv shell

# 显示当前虚拟环境中所有安装包以及它们之间的依赖关系图
pipenv graph

# 更新所有包到最新版本，并自动调整依赖版本锁定文件
pipenv update

# 更新指定包到最新版本，并自动调整依赖版本锁定文件
pipenv update [<包名>]

# 删除当前目录下的虚拟环境
pipenv --rm
```

## uv

可以代替pip，可以创建虚拟环境

```shell
# 显示当前已经安装的和可供安装的Python版本
uv python list
# 安装指定的Python版本（注意：安装的Python并非全局可用，在命令行工具中输入Python无反映）
uv python install 3.10 3.11 3.12
# 卸载指定的版本
uv python uninstall 3.10


# 初始化旧的项目
cd example
uv init
# 创建新项目并初始化
uv init new_example
# 注意此时并不会创建环境（编辑器也不会识别到当前项目中的解释器版本），只有安装包时会自动创建环境或者直接用命令：
uv venv
# 默认使用最新的Python版本，也可为环境指定Python版本
uv venv --python 3.11



# 在当前环境中安装包flask
uv add flask
```



# 模块搜索路径

```python
# python会在sys.path中搜索包
import sys
print(sys.path)

# 谁控制sys.path? 正是PYTHONPATH这个环境变量
# python test.py
# sys.path = ['test.py的路径', 'python基本环境', 'PYTHONPATH包含的路径']
# PYTHONPATH = $PYTHONPATH:/home/tanght/haha:/home/tanght/hehe

# python -m test.py
# sys.path = ['python基本环境', 'PYTHONPATH包含的路径']

# 直接修改sys.path也可以
sys.path.append('/home/tanght/haha')

# 有时候sys.path中带有'.'(点，当前目录)，意思就是当前程序的工作目录
```



# 自定义字典

```python
# 会调用b的__contains__(self, key)方法，key为a
a in b

# 如果一个类定义了__getitem__(self, key)方法，那么他的实例对象（假设为P）就可以这样P[key]取值

# __getitem__(self, key)                  a['key']
# __getitem__(self, key, value)           a['key'] = 10
# __delitem__(self, key)                  del a['key']
```



# 枚举

```python
# IntEnum 可以与int进行 == 比较
# Enum 不可与 int 进行比较，若比较，则一直返回false
# 用unique装饰的枚举class，不能出现重复的value
from enum import Enum, IntEnum, unique

@unique
class EnumColour(IntEnum):
    Red = 1
    Green = 2
    Blue = 3
    Black = 4
    
    # pylint: disable=no-member
    @classmethod
    def value_valued(self, value):
        return value in self._value2member_map_
    
    @classmethod
    def key_valued(self, key):
        return key in self.__members__
    # pylint: enable=no-member
    
print(2 == EnumColour.Green)  			# True
print(EnumColour.value_valued(2))  		# True
print(EnumColour.key_valued("Blue"))  	# True
```



# with语法

定义了`__enter__()`与`__exit__()`函数的类，可以使用with语句，进入with作用域之前会执行`__enter__()`函数，离开with作用于之时会调用`__exit__()`函数，不管with代码块中用户写的代码出现什么异常，离开with代码块时，都会执行`__exit__()`函数。

```python
with expression as var:
    # 一些代码
```

- 首先执行expression，且expression必须返回一个对象
- expression返回的对象必须带有`__exit__()`与`__exit__()`方法
- 执行expression返回的对象的`__exit__()`方法
- `__exit__()`方法返回的内容赋值给var
- 执行with作用域中用户写的代码
- 离开with作用域，并执行`__exit__()`方法

```python
class Test:
    def __init__(self):
        print('init...')
    
    def __enter__(self):
        print('enter...')
        return 'haha'

    def __exit__(self, a, b, c):
        print('exit...')

if __name__ =='__main__':
    with Test() as t:
        print(f't is {t}')
    print('已经离开with代码块啦~')

# 运行结果：
# init...
# enter...
# t is haha
# exit...
# 已经离开with代码块啦~

# 解释：
# with Test() as t:   这个with语句的表达式为  Test()
# Test()这句代码的返回值就是一个Test对象(匿名对象)，且这个对象带有__enter__与__exit__方法
# 执行这个对象的__enter__方法，返回值为"haha"
# 将"haha"这个字符串赋值给t
# 进入with代码块，执行用户的代码
# print(t)  t为"haha"，所以打印出"haha"
# 离开with代码块
# 执行__exit__
```







作用域

```python
with open('123.txt', 'w') as f:
    a = 'haha'
    f.write('123')
print(a)		# ok! with并没有为变量a创建新的作用域，with缩进之外依然可以访问到变量a
f.write('456')	# 不ok！ f只在with缩进范围内生效。缩进范围外已经关闭了（执行了__exit__()）
```







# metaclass与`__new__`



```python
class mymetaclass(type):
    def __new__(self_cls, name, base, attrs):  # self_cls就是他自己，即<class mymetaclass>
        print('mymetaclass __new__', self_cls, name, base, attrs)
        cls = super().__new__(self_cls, name, base, attrs)  # 这步将会创建<class test>，注意不是<object test>
        # 标记1，这里可以修改cls哦，与在标记2处修改效果一样
        # create_cls.haha = '123'   添加了一个静态属性haha，相当于定义class的时候添加了一个静态属性
        # class test:
        #     haha = "123"
        return cls
    
    def __init__(create_cls, name, base, attrs):  # 这里的create_cls是__new__的返回值，即<class test>
        print('mymetaclass __init__', create_cls, name, base, attrs)
        # 标记2，这里可以修改create_cls哦，与在标记1处修改效果一样
        # create_cls.haha = '123'   添加了一个静态属性haha，相当于定义class的时候添加了一个静态属性
        # class test:
        #     haha = "123"
        super().__init__(name, base, attrs)


class test(metaclass=mymetaclass):
    def __new__(cls, *args, **kwargs):
        print('test __new__', cls, args, kwargs)

        return super().__new__(cls, *args, **kwargs)
    
    def __init__(self, *args, **kwargs):
        print('test __init__', self, args, kwargs)


t = test()

# mymetaclass.__new__
# mymetaclass.__init__
# test.__new__
# test.__init__

# mymetaclass的__new__()和__init__()创建<class test>
# <class test>()创建t
```



# PIP

## pip源地址更换

### 临时更换

只对本条pip命令生效

```shell
pip install abc_name -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com
```

### 永久更换

对本台计算的所有pip命令都生效

#### windows

在user目录中创建一个pip目录，如：C:\Users\zhangsan\pip，然后新建pip.ini文件，文件内容如下：

```shell
[global]
index-url = https://pypi.tuna.tsinghua.edu.cn/simple
[install]
trusted-host = https://pypi.tuna.tsinghua.edu.cn
```

#### Linux

修改~/.pip/pip.conf文件（没有就创建一个文件夹及文件）

```shell
[global]
index-url = https://pypi.tuna.tsinghua.edu.cn/simple
[install]
trusted-host = https://pypi.tuna.tsinghua.edu.cn
```

# sqlalchemy

```python
# 创建数据库引擎
from sqlalchemy import create_engine
# 数据库类型+数据库连接工具://用户:密码@数据库IP地址:数据库端口号/数据库名
# 创建数据库引擎，现在还没有连接，不到逼不得已的时候，sqlalchemy不会连接数据库
engine = create_engine('mysql+pymysql://root:123456@localhost:3306/test1', echo=True)

# 创建映射基类
from sqlalchemy.ext.automap import automap_base
base = automap_base()
base.prepare(engine, reflect=True) # 开始映射（从数据库反射表的信息，创建ORM的Class）
# classes是{table_name : ORMClass}
for i in base.classes.keys():
    print(i) # 打印表名

# 从数据库的映射中取得user_info这张表 
user_info = base.classes.user_info





# 会话
# create_engine创建连接池
from sqlalchemy import create_engine
engine = create_engine('mysql+pymysql://root:123456@localhost:3306/test1', echo=True, , max_overflow=0, pool_size=1, pool_timeout=30, pool_recycle=3600)
# 查看连接池状态
print(engine.pool.status())
# Pool size: 1  Connections in pool: 1 Current Overflow: 0 Current Checked out connections: 0
# sessionmaker创建session工厂sm
from sqlalchemy.orm import sessionmaker
sm = sessionmaker(bind=engine)
# 实例化sm创建一个session，此时还不需要从连接池中获取连接
session = sm()
session.add(tmp)
# 现在session会从连接池中获取一个连接，用于执行SQL语句
session.commit()
# 还回连接，必须close
session.close()
```



# 小乌龟

```python
import turtle


turtle.setup(1024, 800, 100, 80) # 设置turtle的窗口属性，turtle窗口大小为1024*800，窗口左上角位于电脑屏幕的（100，80）处，电脑屏幕的左上角为（0，0）


# turtle中的颜色共三种表示方式，英文代码，RGB格式，16进制格式
turtle.bgcolor("LightPink") 			# 设置画布背景颜色，英文代码
turtle.bgcolor((0.255, 0.182, 0.193))	# 设置画布背景颜色，RGB格式，必须统一到0-1之间
turtle.bgcolor("#FFB6C1")				# 设置画布背景颜色，16进制格式


turtle.pencolor("red") 	# 设置笔的颜色
turtle.speed(10) 		# 设置笔的速度，[0,0.5]最快，根本不出过程，直接出最终结果。(0.5,1]为减速。(1,10]为加速
turtle.pensize(10)		# 设置笔刷的宽度，默认为1
turtle.pendown()		# 放下笔刷，笔移动的话就会画图了
turtle.penup()			# 抬起笔刷，笔移动的话不会画图，因为笔刷已经抬起来了
turtle.goto(100, 100)	# 画笔移动到（100，100）处，屏幕中心为（0，0）
turtle.forward(100)		# 向当前画笔方向移动100像素长度
turtle.backward(100)	# 向当前画笔相反方向移动100像素长度
turtle.right(30)		# 顺时针旋转30°
turtle.left(30)			# 逆时针旋转30°
turtle.dot()			# 在当前画笔位置画一个点，点的大小为笔刷的大小，点的颜色为笔刷的颜色
turtle.dot(5, "red")	# 在当前画笔位置画一个点，点的大小为5.颜色为red
turtle.pos()			# 返回笔刷当前位置
turtle.heading()		# 返回笔刷当前角度
turtle.hideturtle()		# 隐藏小乌龟
turtle.showturtle()		# 显示小乌龟
turtle.isvisible()		# 返回小乌龟是否可见
turtle.shape("turtle")	# 设置笔刷形状

```



# 正则

## re.Match对象

re.Match对象为一些re.api的返回值，有必要了解一下它的使用。python的正则表达式库通过re.Match对象来跟调用者交流。当我们写好一个正则表达式如：**'a([0-9]+)b([0-9]+)c'**，将他交给re.match或re.search等函数时。如果匹配成功了，函数将返回一个re.Match对象，我们通过操作re.Match来获取我们想要的东西。比如获取第一个捕获分组的内容group(1)；获取所有捕获分组的内容groups()；正则表达式匹配到的所有内容（捕获分组和非捕获分组都要）group(0)；

```python
# 通过 标签名 获取分组捕获指定分组的内容，前提是正则表达式中设置了分组捕获的名字(?P<any_name>)
result = obj.group('Name')

# 通过 位置 获取分组捕获指定分组的内容分
# group(0) 正则表达式匹配到的所有内容，即使正则表达式没有使用分组捕获，group(0)也可以用
# group(1) 正则表达式 分组捕获 的第一组内容
# group(2) 正则表达式 分组捕获 的第二组内容
# group(N) 正则表达式 分组捕获 的第N组内容
# groups() 元祖，元祖的每一个元素是一个捕获分组的内容
obj.group(0)
obj.group(1)
obj.group(2)
obj.group(N)


s = '(?P<string>[a-z]+)([\d]+)'
obj.group('string')  	# 返回([a-z]+)这部分
obj.group(1)         	# 返回([a-z]+)这部分
obj.group(2)			# 返回([\d]+)这部分


s = '(?P<string>[a-z]+)[\d]+'
obj.group('string')		# 返回([a-z]+)这部分
obj.group(1)			# 返回([a-z]+)这部分
obj.group(2)  			# 错误，正则表达式没有将[\d]+记录为第二部分，因为没加括号
```

## 捕获分组

什么是分组？

加了括号的正则表达式就叫分组了，几个括号就是分了几组

为什么要分组？

因为我们多一个字符串中的其它部分不感兴趣，只对某些部分感兴趣，所以将感兴趣的放到分组中，匹配成功之后直接按组获取，这样就能直接获取到我们感兴趣的地方了

如何编写分组的正则表达式？

```python
p1 = '([a-z]*)(?P<year>[0-9]{4})-(?P<month>[0-9]{2})-(?P<day>[0-9]{2})([a-z]*)'
p2 = '([a-z]*)(?P<year>[0-9]{4})-(?P<month>[0-9]{2})-(?P<day>[0-9]{2})[a-z]*'
```

p1与p2的匹配模式完全相同，只是在匹配成功时的返回值不同，p1有5组，p2只有4组

p1_result.groups()会返回一个带有5个元素的元祖

p2_result.groups()会返回一个带有4个元素的元祖

groupdict()返回带名字的组(不包含不带名字的组)，是一个字典

group(1)按照组的序号来取内容

group('name')按照组的名字来取内容

group()返回这个字符串中，符合正则表达式的，那部分字符串

## 分割字符串

在python进行字符串分割一般使用**str.split()**函数，比如将字符串**"abc:123:xyz"**以冒号进行分割，以列表的形式将分割后的结果返回给调用者**["abc", "123", "xyz"]**

re库也提供了类似的功能，且比python内置的str.split()函数更加强大

### re.split

```python
re.split(pattern, string, maxsplit=0, flags=0)
```

- 功能：以pattern为分隔符，分割string，最多进行maxsplit次分割
- 参数：
  - pattern：正则表达式
  - string：待分割的字符串
  - maxsplit：最大分割（切刀）次数（切1刀，分成2部分。切2刀，分成3部分，类推...）
  - flags：正则表达式标志位
- 返回值：

#### 示例

```python
# 使用pattern模式对string进行分割，最多分maxsplit次，返回list
# maxsplit默认为0，表示不限制分割次数
re.split(pattern, string, maxsplit=0, flags=0)

# 使用数字对字符串进行分割
s = r'abc123qaz3wsx4edc12345rfv'
result = re.split('[0-9]+',s)
#result：['abc', 'qaz', 'wsx', 'edc', 'rfv']

# 使用多个不同的字符对字符串进行分割，将字符用|连接起来就行了
s = r'qaz,wsx.edc~rfv%tgb'
result = re.split(',|\.|~|%',s)
# result：['qaz', 'wsx', 'edc', 'rfv', 'tgb']

# 使用两个逗号，或者两个句号进行分割
s = r'qaz,wsx.edc,,rfv...tgb'
result = re.split(',,|\.\.',s)
# result：['qaz,wsx.edc', 'rfv', '.tgb']
```

## 正则表达式标志位

| 标志位         | 作用                                                         |
| -------------- | ------------------------------------------------------------ |
| re.I（小写爱） | 使匹配对大小写不敏感                                         |
| re.L           | 做本地化识别（locale-aware）匹配                             |
| re.M           | 多行匹配，影响 ^ 和 $                                        |
| re.S           | 使 . 匹配包括换行在内的所有字符                              |
| re.U           | 根据Unicode字符集解析字符。这个标志影响 \w, \W, \b, \B.      |
| re.X           | 该标志通过给予你更灵活的格式以便你将正则表达式写得更易于理解 |

## 替换

### re.sub

```python
re.sub(pattern, repl, string, count=0, flags=0)
```

- 功能：扫描string，发现pattern匹配成功的部分就进行一次repl替换（用repl函数的返回值，替换匹配到的部分），直到string结尾。
- 参数：
  - pattern：正则表达式
  - repl：替换函数（或者字符串），这个函数接受一个re.Match类型的参数，返回一个字符串
  - string：待操作的字符串
  - count：最大替换次数
- 返回值：替换后的字符串

#### 示例

```python
# 参数match：re.Match对象
def myfun(match):
    str_number = match.group('number')
    int_number = int(str_number)
    return str(int_number + 111)

s = r'abc123qaz321'
# re.sub使用 '(?P<number>[\d]+)' 来对 s 进行扫描，每次成功匹配的时候就生成一个 re.Match 对象，传递给myfun的参数，然后运行myfun函数，使用myfun函数的返回值替换掉匹配成功的部分，继续向后扫描
result = re.sub('(?P<number>[\d]+)', myfun, s)
```

## 匹配与提取

### re.match

```python
re.match(pattern, string, flags=0)
```

- 功能：按照pattern**从头**开始匹配string（**重点是从头开始匹配**，若第一个字符匹配失败，则认为不匹配，即便从string的中间部分可以找到与pattern相匹配的部分），匹配失败或者成功都立即返回，不向后继续匹配
- 参数：
  - pattern：正则表达式
  - string：待匹配的字符串
  - flags：正则表达式标志位
- 返回值：
  - 匹配成功：Match对象
  - 匹配失败：None

#### 示例

```python
def myfun(s):
    result = re.match('abc[\d]+', s)
    if result is None:
        print('匹配失败')
    else:
        print('匹配成功')
        print(result.group(0))  # 匹配成功后，可以查看匹配到的具体内容，group(0)为正则表达式匹配到的所有内容

s1 = 'abc12345xxxabc876'
s2 = 'babc12345xxxabc876'
myfun(s1)	#匹配成功，并且打印出具体内容
myfun(s2)	#匹配失败，因为第一个字符为b，而正则表达式要求第一个字符为a
```

### re.search

```python
re.search(pattern, string, flags=0)
```

- 功能：按照pattern匹配string，**不必从头开始**，从任何部分开始匹配都可以
- 参数：
  - pattern：正则表达式
  - string：待匹配的字符串
  - flags：正则表达式标志位
- 返回值：
  - 匹配成功：Match对象
  - 匹配失败：None

#### 示例

```python
pass
```

### re.findall

```python
re.findall(pattern, string, flags=0)
```

- 功能：按照pattern开始扫描string（不必从头开始，从任何位置开始都行），遇到匹配成功的部分，则记录到返回值中，继续向后匹配，一直到字符串的结尾
- 参数：
  - pattern：
  - string：
  - flags：
- 返回值：
  - 匹配成功：
    - pattern中使用了捕获分组：元祖列表，[(,),...]。元祖中的每个元素是捕获列表中的某一组
    - pattern中未使用了捕获分组：字符串列表，[str,...]。字符串即为匹配到的值
  - 匹配失败：空list

#### 示例

```python
pass
```

# 调用c语言动态库

首先，64位的python3只能调用64位的c库，64位的python3不能调用32位的c库。32位的python3能调用32位的c动态库与64位的c动态库。python2没试过。

```python
from ctypes import CDLL, WinDLL
import ctypes

try:
    lib = WinDLL(r'C:\MyFirstDll.dll') # 加载动态库
    add = lib.ThtAdd				#获取动态库中的ThtAdd函数
    add.restype = ctypes.c_double	# 告诉python，这个函数的返回值类型是c语言类型的double
    a = ctypes.c_double(10)
    b = ctypes.c_double(20)
    print(add(a, b))				# 传入两个c语言类型的double
except Exception as e:
    print(e)
```



# class中的 \__contains__(self, value)

使用in，会调用类中的\__contains__方法

```python
class tanght:
    def __contains__(self, key):
        print('1')
        return False

t = tanght()
print('a' in t)
```



# \_\_iter\_\_(self)与\_\_next\_\_(self)

迭代器\_\_iter\_\_(self)返回一个带有\_\_next\_\_(self)方法的对象，一般是一个对象同时定义这两个方法，\_\_iter\_\_(self)直接返回self就行了，因为self就有next方法啊

for i in xxx时，会先调用xxx的\_\_iter\_\_方法，\_\_iter\_\_方法会返回一个对象，然后每次for就调用一次这个对象的\_\_next\_\_方法，\_\_next\_\_方法的返回值赋值给i

```python
class test():
    def __init__(self,data=1):
        self.data = data

    def __iter__(self):
        return self
    def __next__(self):
        if self.data > 5:
            raise StopIteration
        else:
            self.data+=1
            return self.data

for item in test(3):
    print(item)
```

# str.translate

```python
s = '123'
a = b'haha...' # 假装一共256个字符
# s中的字符，按照a中的字符转换，转换的原理是
s1 = s.translate(a)
```

# 字符串拼接

key：拼接，模板，插值，大括号

```python
s1 = 'tanght'
s2 = f'Hello {s1}'
```

# 字符串编码解码

先了解一下python中如何表示字节流

我们知道，任何数据在计算机中都是0和1的流，俗称比特流。但是我们与计算机打交道的时候更愿意用字节来描述信息(1字节=8比特)。比如你可以向计算机申请1字节的内存，然后计算机将内存条上的8个比特给了你，你可以随意操作这8个比特。你可以将`0000 0000`这8个bit储存其中，也可以将`1111 1111`储存其中，你高兴就好。但是你不能向计算机申请0.5个字节的内存，因为申请的内存只能是1字节的整数倍。

那么在python中，字节流是如何表现的呢？`a = b'\x00\x01\x03\xff'`这样python就会给你4个字节的内存，并初始化为`00000000 00000001 00000011 11111111`

当你用十六进制表示内存中的字节流时，不用考虑"有符号\无符号\补码"等相关信息，因为根本不是同一个问题。`\x00`永远是`00000000`，`\xff`永远是`11111111`

```python
# 创建一个字符串"唐"，至于他在内存中是什么格式的二进制流，与python默认的编码格式有关，我们不用关心
a = "唐"  

# 将"唐"的utf-8字节流返回给我，b的类型是bytes(字节流)
b = a.encode('utf-8')
print(len(b))  # 3 也就是说"唐"这个字符，使用utf-8编码的话，在内存中是要占用3个字节(24bit)的
print(b[0], b[1], b[2])  # 229 148 144 换算成16进制就是 e5 94 90

c = a.encode('gbk')
print(len(c))  # 2 也就是说"唐"这个字符，使用gbk编码的话，在内存中是要占用2个字节(16bit)的
print(b[0], b[1])  # 204 198 换算成16进制就是 cc c6
```



```python
# 创建字节流
a = bytes([229, 148, 144])  # 创建字节流，包含3个字节，数组中的元素必须在0-255之间，否则bytes()函数出错
a = bytes([0xe5, 0x94, 0x90])  # 跟上面是同一个意思，只不过是用16进制表示
a = b'\xe5\x94\x90'  # 跟上面是同一个意思

# 将a这个字节流，按照utf-8规则解释成字符串
b = a.decode('utf-8')  # b = "唐"

# 将a这个字节流，按照gbk规则解释成字符串
try:
    b = a.decode('gbk')  # 出错，[229, 148, 144]这三个字节无法按照gbk解释，即使能解释，肯定也不是"唐"这个字符
except Exception:
    pass
```



a.encode('utf-8')将字符串a的utf-8格式的字节流返回给我

b.decode('utf-8')将字节流b按照utf-8规则解释成字符串



```python
class PostCleaner(DictField):
    game_id = IntField(min=0)  # 大于等于0的整数
    country_id = ListField(item=IntField())  # 整数列表
    force = F_field.IntField(default=0)  # 默认值
    version = VersionField(sname='app_version')  # 重命名
    other = OtherCleaner()  # 嵌套结构
```

# 离线安装

```shell
# 先用可以联网的电脑下载，下载下来的可能是压缩包，也可能是.whl
pip download -d C:\Users\tanght\Desktop\tmp\package -r r.txt
# r.txt就是依赖文件  pip freeze来的

# 然后去不能联网的电脑上安装，多两个参数而已--no-index --find-links=
pip install --no-index --find-links=/haha/hehe pymysql
```

# 代理内网

```shell
sudo pip3 install redis -i https://pypi.tuna.tsinghua.edu.cn/simple --proxy=192.168.96.67:8888 --trusted-host pypi.tuna.tsinghua.edu.cn
```

```
# Windows机器使用违法的VPN, 哈哈
pip install -r requirements.txt --proxy=127.0.01:7890
```

# 浏览器自动化

## Playwright

浏览器自动化工具，类似以前爬虫时用的selenium，但是比selenium好用100倍。

它是一个没有页面的软件，可以用pip安装，也可以用npm安装，还可以用其它语言的包管理器安装。

### 安装

安装这个软件，安装之后是一个可执行文件，在python的软件包目录下

pip install playwright

playwright安装完之后，还需要让playwright自己下载各种浏览器的内核

playwright install

### 打开浏览器

**1. 使用 connect_over_cdp 连接已经运行的 chrome 浏览器**

相比直接使用 自己的浏览器，这种方法更像人类

```python
# 1. 模拟鼠标双击，打开chrome浏览器，启动参数中输入--remote-debugging-port=9222
# 这个启动参数会让chrome接受远程控制，否则的话无法用playwright来控制浏览器
cmdarg = [self.config.chrome_instance_path, '--remote-debugging-port=9222']
popenarg = {
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL,
}
subprocess.Popen(cmdarg, **popenarg)
sleep(100)
playwright = await async_playwright().start()

# 2. 使用 playwright 连接已经启动好了的浏览器
playwright.chromium.connect_over_cdp(endpoint_url='http://localhost:9222', timeout=20000)

# 3. 执行反反爬虫js脚本来设置一些浏览器参数，避免被反爬虫
```

**2. 使用 playwright 自带的浏览器**

playwright 安装完之后，playwright install 命令是让 playwright 安装自己的浏览器，所以即使用户没有安装 chrome 浏览器，playwright 也能使用

```python
```



# 数据校验

## pydantic

### 基础

继承BaseModel

```python
from pydantic import BaseModel

# 优点, 继承BaseModel就不用写__init__方法了
# 优点, 类型检查, 类型转换, 类型提示
class User(BaseModel):
    name: str
    age: int
    email: str
    
user1 = User(name="tht", age="30", email="xx@qq.com")  # pydantic自动将age转换为int, 能转尽量转, 转不了就抛出异常
user2 = User(name="tht", age="a30", email="xx@qq.com")  # a30不能转为int, 所以会抛出异常
```

### 选填

from typing import Optional

```python
from typing import Optional
from pydantic import BaseModel, EmailStr

class User(BaseModel):
    name: str
    age: int
    email: EmailStr
    phone: Optional[str] = None # Optional选填字段, 如果没填，则用默认值代替

user1 = User(name="tht", age=30, email="xx@qq.com")  # name='tht' age=30 email='xx@qq.com' phone=None
# user2 = User(name="tht", age=30, email="abcdefg")  # 无效的电子邮件，抛出异常

```

### 自定义验证

使用field_validator装饰器

```python
from typing import Optional
from pydantic import BaseModel, EmailStr, field_validator

class User(BaseModel):
    name: str
    age: int
    email: EmailStr
    phone: Optional[str] = None

    @field_validator("age") # 检查age字段
    def check_age(cls, value):
        if value < 18:
            raise ValueError("用户年龄必须大于18岁")
        return value
    
user1 = User(name="tht", age=17, email="xx@qq.com") # 错误

```

### Field

附加信息和约束

Field第一个参数为默认值，如果第一个参数为`...`则表示此字段没有默认值，用户必须手动填写

```python
from typing import Optional
from pydantic import BaseModel, EmailStr, Field

class User(BaseModel):
    name: str
    age: int = Field(..., description="用户年龄", gt=1, lt=100)
    email: EmailStr
    phone: Optional[str] = None

    
user1 = User(name="tht", age=100, email="xx@qq.com") # 错误
print(user1)
```

- **默认值 / 必填标识：**Field("默认名称")或Field(...)
- **description：**提供字段的描述信息，用于生成 API 文档等，`description="i am age"`
- **title：**为字段指定标题，同样用于文档展示，`title="Age"`
- **alias：**定义别名，在序列化或反序列化过程中使用别名，`alias="user_age"`
- **约束条件：**gt、ge、lt、le、min_length、max_length、regex
- **default_factory：**接收一个无参工厂函数，用于动态生成默认值，示例：`default_factory=list` 意味着默认值为一个空列表。
- **const：**如果为 True，则要求传入的值必须与默认值一致，也可以不填写，那就用默认值。示例：`const=True`。
- **exclude, include：**控制序列化时的输出，可以配置哪些字段在 dict 或 JSON 输出时被包含或排除。

### ConfigDict

ConfigDict可以控制整个数据的规则

```python
from pydantic import BaseModel, ConfigDict

class MyModel(BaseModel):
    # 整个class的规则
    model_config = ConfigDict(
        arbitrary_types_allowed=True, # 允许字段指定非 Pydantic 内置支持的任意类型（比如函数、第三方对象、或自定义类）
        extra='forbid', # "allow"：保留所有额外字段。 "ignore"：忽略（不保存）额外字段。 "forbid"：如果输入额外字段则报错
        populate_by_name=True, # 允许在模型实例化时，即使定义了别名，也可以使用原始字段名称赋值
        alias_generator=lambda field_name: field_name.upper(),  # 定义一个函数，用于自动生成字段的别名
        json_encoders={CustomType: lambda v: str(v)}, # 为自定义类型提供 JSON 序列化函数
        validate_assignment=True, # 启用对模型实例中属性的赋值进行验证
        frozen=True,
        copy_on_model_validation=True,
        from_attributes=True,
        use_enum_values=True, # 在处理 Enum 类型字段时，使用枚举的值而非枚举对象本身
        error_msg_templates={'value_error.missing': '字段 {loc} 是必填的'}, # 自定义验证错误的消息模板
        json_schema_extra={"examples": [{"id": 1, "name": "example"}]},
        json_dumps=lambda v, *, default: __import__('json').dumps(v, default=default),
        json_loads=__import__('json').loads,
        smart_union=True, # 在处理联合类型（Union）字段时，使用更智能的方式来匹配输入数据，从而减少不必要的验证错误
    )
    
    # 各个字段的规则
    id: int
    name: str
```

# 函数参数

python的函数规则简直是一坨屎，超级TMD混乱，python再发展几年，就得用毛笔在屏幕上画画了！垃圾、垃圾、垃圾！！！FUCK FUCK FUCK！

我认为最好的语言就是---->完成一件事只有一种办法，这样所有人就TM统一了，不用猜别人的代码了！像他妈python这种语言竟然他妈的火了，简直是灾难！

## 传参方式

### 按位置传参

这是最简单的方式，根据参数在定义时的位置依次传递。

```python
def add(x, y):
    return x + y

# 按位置传参
result = add(1, 2)  # x=1, y=2
```

###  按关键字传参

在调用时明确指定参数名，这样的好处是顺序可以不固定，并且代码可读性更高。

```python
result = add(x=1, y=2)
result = add(y=2, x=1)
```

### 位置和关键字混用

可以同时使用，但必须注意：**位置传参必须出现在关键字传参之前**。

```python
def greet(greeting, name):
    print(f"{greeting}, {name}")

greet("Hello", name="Alice")  # "Hello"作为第一个位置参数，name通过关键字传入
```

## 参数定义

### *args

收集额外的位置参数。

前面一个星号（*）表示把传入的额外位置参数收集到一个元组中。

```python
def func_with_args(x, *args):
    print(x)      # 第一个位置参数
    print(args)   # 其余所有位置参数以元组形式保存

func_with_args(10, 20, 30, 40)  
# 输出：
# 10
# (20, 30, 40)
```

### **kwargs

收集额外的关键字参数。

两个星号（**）表示把传入的额外关键字参数收集到一个字典中。

```python
def func_with_kwargs(x, **kwargs):
    print(x)
    print(kwargs)  # 多余的关键字参数以字典形式保存

func_with_kwargs(10, a=1, b=2)  
# 输出：
# 10
# {'a': 1, 'b': 2}
```

### 单独的星号 *

限制后续参数必须以关键字方式传递。

在函数参数列表中只写一个单独的星号，后面的所有参数都将成为**关键字专用参数**。

```python
def func_keyword_only(a, b, *, option=True):
    print(a, b, option)

func_keyword_only(1, 2, option=False)  # 正确
# func_keyword_only(1, 2, False)  -> 错误，因为 option 必须以关键字形式传递
```

### 位置分隔符/

位置专用参数（Python 3.8+）。

在参数列表中使用 `/` 分隔符，位于其左侧的参数只能通过位置传入。

```python
def func_positional_only(a, b, /, c, d):
    print(a, b, c, d)

func_positional_only(1, 2, c=3, d=4)  # a, b 必须为位置参数
# func_positional_only(a=1, b=2, c=3, d=4)  -> 错误
```

## *和**解包

### 用 `*` 解包序列

把一个列表或元组的值依次传递给函数的对应位置参数。

```python
def multiply(a, b, c):
    return a * b * c

nums = [2, 3, 4]
result = multiply(*nums)   # 相当于 multiply(2, 3, 4)
```

### 用 `**` 解包字典

```python
def introduce(name, age):
    print(f"My name is {name} and I am {age} years old.")

info = {'name': 'Alice', 'age': 30}
introduce(**info)  # 相当于 introduce(name='Alice', age=30)
```

# 类型注解

类型注解只用于编辑器的代码检查和智能提示，python运行时会忽略类型注解

```python
from typing import Callable, Dict, Type


variable_name: Type = value
```

## 变量注解

可以直接在变量声明时标注变量的类型。即使不赋初值，类型注解也能帮助 IDE 和静态检查工具了解变量的预期类型。

```python
x: int = 42         # x 应为整数，默认值 42
name: str = "Alice" # name 应为字符串，默认值 "Alice"
score: float        # score 预计为浮点型，但目前未赋值
```

## 函数参数与返回值注解

在函数定义时，可以为每个参数指定类型，使得函数使用者明确知道传入参数的预期类型。

```python
def add(a: int, b: int) -> int:
    return a + b
```

在上面的代码中：

- 参数 `a` 和 `b` 被标注为整数（`int`）。
- 箭头后的 `int` 表示返回值也必须是整数。

## 容器类型注解（ `typing` 模块）

指定容器内元素进行类型

### List

```python
from typing import List

numbers: List[int] = [1, 2, 3, 4]
names: List[str] = ["Alice", "Bob", "Charlie"]
```

### Dict

用于指定字典中键值的类型，比如键是字符串，值是整数。

```python
from typing import Dict

user_ages: Dict[str, int] = {"Alice": 25, "Bob": 30}
```

### Tuple

用于标注固定长度且各元素类型已定的元组。

```python
from typing import Tuple

coordinate: Tuple[float, float] = (10.0, 20.5)
```

## Optional

`Optional[T]` 表示类型 `T` 或 `None`，与 `Union[T, None]` 等价。常用于标识参数或返回值可能为空。

```python
from typing import Optional

def find_user(user_id: int) -> Optional[str]:
    # 如果未找到用户，返回 None
    if user_id != 1:
        return None
    return "Alice"
```

也可用于变量声明：

python

```
phone: Optional[str] = None  # 可能为字符串，也可能是 None
```

## Union

`Union[A, B]` 用于指明变量或参数可能为 A 或 B 中的任一类型。

```python
from typing import Union

def stringify(data: Union[int, float]) -> str:
    return str(data)
```

在这个例子中，`data` 可以是整数或浮点数。

## Any

当你不希望进行类型限制或者类型不确定时，可以使用 `Any`。

```python
from typing import Any

def process(item: Any) -> None:
    print("Processing:", item)
```

## Callable

用于标注可调用对象（例如函数）。

```python
from typing import Callable

def operate(func: Callable[[int, int], int], a: int, b: int) -> int:
    return func(a, b)

# 示例函数
def multiply(x: int, y: int) -> int:
    return x * y

result = operate(multiply, 3, 4)  # 返回 12
```

上面的例子中：

- `Callable[[int, int], int]` 表示一个需要两个整数参数并返回一个整数的函数。

## Type

`Type[XXX]` 表示一个类型对象，这里的 `XXX` 是某个类型（通常为类），`Type[XXX]` 的含义是“**继承自 XXX 的类**”（包括 XXX 自身）。当你希望一个变量、参数或返回值接收的是一个类，**而不是该类的实例时**，就可以使用 `Type[XXX]`。

```python
from typing import Type

class User(BaseModel):
    name: str
    age: int

def print_schema(model: Type[BaseModel]) -> None:
    # model 必须是 BaseModel 的子类，故可以调用其 .schema() 类方法
    print(model.schema())

print_schema(User) # User类，而不是User对象
```

在这个例子中：

- 参数 `model` 的类型被注解为 `Type[BaseModel]`，表示传入的必须是一个继承自 `BaseModel` 的类（例如 `User`），而不是 `User` 的实例。
- 这样确保可以直接调用传入类的类方法，比如 `.schema()`，而不用担心对象实例与类本身的区别。

## 类型别名

通过给复杂的类型签名创建一个别名，可以让代码更简洁易懂。

```python
from typing import List

Vector = List[float]  # 定义一个别名，将表示浮点数列表

def scale(vector: Vector, factor: float) -> Vector:
    return [x * factor for x in vector]

v: Vector = [1.0, 2.0, 3.0]
scaled_v = scale(v, 2.0)
```

# 类属性，实例属性，类型注解

## 类属与实例

```python
class People:
    # 类属性
    species = "Homo sapiens"

    def __init__(self, name, age):
        # 实例属性
        self.name = name
        self.age = age
  
    def speak(self):
        print(f"{self.name} 说: 我 {self.age} 岁。")

p1 = People("Alice", 30)
p2 = People("Bob", 25)

# 访问实例属性
print(p1.name)  # 输出: Alice
print(p2.age)   # 输出: 25

# 访问类属性
print(People.species)  # 输出: Homo sapiens
print(p1.species)      # 输出: Homo sapiens

# 修改类属性会影响所有实例
People.species = "H. sapiens"
print(p1.species)      # 输出: H. sapiens
print(p2.species)      # 输出: H. sapiens

# 修改实例属性仅影响当前实例
p1.name = "Alice Smith"
print(p1.name)         # 输出: Alice Smith
print(p2.name)         # 输出: Bob
```

## 实例属性覆盖类属性

可以在`__init__`函数中覆盖类属性

尽管覆盖了类属性，也能通过Class.XXX来获取类属性

```python
class People:
    # 类属性：所有People实例共享
    species = "Homo sapiens"

    def __init__(self, name, age):
        # 实例属性：每个实例单独拥有
        self.name = name
        self.age = age
  
    def speak(self):
        print(f"People {self.name} 说: 我 {self.age} 岁。")


class Dog:
    # 类属性：所有Dog实例初始共享（值为 "Homo sapiens"）
    species = "Homo sapiens"

    def __init__(self, name, age):
        # 实例属性：覆盖了类属性
        self.name = name
        self.age = age
        # 此处将实例属性 species 赋予一个不同的值，这会遮蔽类属性 Dog.species
        self.species = "haha"
  
    def speak(self):
        print(f"Dog {self.name} 说: 我 {self.age} 岁。")

        
# 测试对比代码
# People类
p1 = People("Alice", 30)
p2 = People("Bob", 25)

print("===== People 类 =====")
# 访问实例属性，在People中，没有为species赋予实例属性，因此访问的是类属性
print("p1.species:", p1.species)     # 输出: Homo sapiens
print("p2.species:", p2.species)     # 输出: Homo sapiens
print("People.species:", People.species)
p1.speak()
p2.speak()

# Dog类
d1 = Dog("Buddy", 5)
d2 = Dog("Max", 3)

print("\n===== Dog 类 =====")
# 对于Dog，每个实例在初始化时覆盖了 species 属性，将其设置为 "haha"
print("d1.species:", d1.species)     # 输出: haha
print("d2.species:", d2.species)     # 输出: haha
# 但类属性仍然保持原始值
print("Dog.species:", Dog.species)
d1.speak()
d2.speak()

# 补充说明：
# 如果你删除一个Dog实例的实例属性 species，
# 则它会回退到类属性的值。例如：
del d1.species
print("\n删除 d1 的实例属性 species 后:")
print("d1.species:", d1.species)     # 输出: Dog.species 的值，即 "Homo sapiens"

```

## 类型注解

类型注解与类属性定义差不多，容易混乱，注意区分哪些是**类型注解**哪些是**类属性**。

```python
class Example:
    a: int       # 仅仅是类型注解，不赋初值（不会创建类属性），仅仅用于限制__init__中的a的类型
    b: int = 5   # 类型注解和赋值同时出现（这既是类型注解，也是类属性）
    c = "hello"  # 直接赋值（没有类型注解，仅仅是类属性）

    def __init__(self, a):
        # 在构造函数中，将类型注解中声明的属性实际创建为实例属性
        self.a = a  # 这里创建了实例属性 a，跟上面的类型注解 a 衔接

print(Example.__dict__) # 查看类属性、类方法、类的一些其它属性。注意这里与实例无关
print(Example.__annotations__) # 查看类注解
```

**解释：**

- `a: int`   这是一个“纯类型注解”项，存在于 `Example.__annotations__` 中，但不会出现在 `Example.__dict__` 中。   在实例化时，我们通常会在 `__init__` 里给 `self.a` 赋值，这样每个实例就会有自己独立的 `a` 属性。
- `b: int = 5`   这是一个类属性：
  - 它既有类型注解，也有默认值。
  - 这会在 `Example.__dict__` 中创建一个 `b` 属性，所有实例在没有被覆盖的情况下，都共享这个值。
- `c = "hello"`   没有显式的类型注解，但因为赋值动作，它也是类属性，同样被所有实例共享。

# TYPE_CHECKING

仅用于代码检查的代码

```python
# main.py
from typing import TYPE_CHECKING

# 仅用于类型检查时导入 X，避免在运行时导入，从而解决循环依赖和降低开销
if TYPE_CHECKING:
    from other_module import X

# 在这里，我们使用字符串 "X" 作为前向引用，
# 因为在运行时 main.py 内部不会直接导入 X，
# 但类型检查工具能根据 TYPE_CHECKING 中的导入信息获取 X 的定义。
class Y:
    def __init__(self, x: "X") -> None:
        self.x = x

    def display(self) -> None:
        print(f"Y 里持有的 x：{self.x}")

def process(item: "X") -> None:
    print(f"Processing item: {item}")

if __name__ == "__main__":
    # 在运行时，可以直接从 other_module 导入 X
    from other_module import X

    # 创建一个 X 的实例，并用它来初始化 Y
    x_instance = X(42)
    y_instance = Y(x_instance)
    
    # 调用方法
    y_instance.display()
    process(x_instance)

```

# 泛型

需要使用Generic, TypeVar

TypeVar相当于C++和Go中的[T]

```python
from typing import Generic, TypeVar, List

T = TypeVar('T')

class MyList1(Generic[T]):
    def __init__(self) -> None:
        self.items: List[T] = []

    def add(self, item: T) -> None:
        self.items.append(item)

    def get_first(self) -> T:
        return self.items[0]

list1 = MyList1[int]()
list1.add(1)
list1.add("a") # !!!飘红, 因为list1是MyList1[int], 不能添加字符串
print(list1.get_first())


class MyList2():
    def __init__(self) -> None:
        self.items: List[T] = [] # !!!飘红, 无法使用泛型, 因为MyList2没有继承自泛型

    def add(self, item: T) -> None:
        self.items.append(item)

    def get_first(self) -> T:
        return self.items[0]

list2 = MyList2[int]() # !!!飘红, 无法使用泛型, 因为MyList2没有继承自泛型
list2.add(1)
print(list2.get_first())
```

# 代码静态检查

vscode中开启代码静态检查，否则即使你写了注解，vscode依然不会提示你

![image-20250313211411003](./assets/image-20250313211411003.png)

# 常用装饰器

## @dataclass

python3.7引入的功能，项目代码中常常要定义class，仅仅是为了将一些数据放在一起，并不带有其它逻辑。dataclass可以简化这一步骤。

**不使用 @dataclass：**需要自己写class的`__init__`，`__eq__`，`__repr__`

```python
# 不使用 @dataclass，需要手动编写 __init__、__repr__ 和 __eq__
class Person:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age

    def __repr__(self) -> str:
        # 手动定义了对象的字符串表示，便于调试
        return f"Person(name={self.name!r}, age={self.age!r})"

    def __eq__(self, other: object) -> bool:
        # 手动实现对象相等性比较
        if not isinstance(other, Person):
            return False
        return self.name == other.name and self.age == other.age

    
```

**使用 @dataclass：**与上面的代码等价

```python
from dataclasses import dataclass

@dataclass
class PersonData:
    name: str
    age: int
```

## @staticmethod

将class中指定的函数变为普通函数，与普通函数没有任何区别

与这个class没有一点关系，仅仅是这个函数的位置写在了这个class里

```python
class Calculator:
    @staticmethod
    def add(a, b):
        return a + b

# 使用静态方法，无需创建 Calculator 的实例
result = Calculator.add(10, 20)
print("10 + 20 =", result)  # 输出：10 + 20 = 30
```

## @classmethod

将class中指定的函数变为静态方法，此方法只跟这个class有关系，跟这个class的实例没有关系

```python
class Person:
    # 类属性，用于保存当前已创建的人口数量
    population = 0

    def __init__(self, name):
        self.name = name
        Person.population += 1

    @classmethod
    def create_anonymous(cls):
        """
        作为工厂方法，用于创建匿名用户。
        这里使用 cls 而不是直接指定 Person，这样子类调用时依然有效。
        cls 就是 Person。
        """
        return cls("匿名")

    @classmethod
    def get_population(cls):
        """
        返回当前由此类创建的实例总数。
        """
        return cls.population

# 使用普通构造方法创建实例
person1 = Person("Alice")
# 使用类方法作为辅助构造器创建匿名用户
person2 = Person.create_anonymous()

print("当前人口数量：", Person.get_population())  # 输出：当前人口数量： 2
```

## @property

- property装饰器就是其它语言中的getter和setter函数。
- 逼不得已不要使用这个属性，写个get函数并不会将你累死。
- 如果你使用这个装饰器，会造成你不知道哪些属性是"真属性"，哪些属性是"假属性".
- 你读取一个属性的时候，它TMD它会执行一堆逻辑，甚至会抛出异常。
- 你调试的时候都不知道到底要F10还F11，这个属性简直是灾难。
- 逼不得已的情况：旧代码获取这个属性是直接读取的，现在读取这个属性需要增加一些逻辑，这时候使用property将逻辑隐藏在这个属性的背后，可以做到兼容旧代码。

```python
class Temperature:
    def __init__(self, celsius):
        self._celsius = celsius

    @property
    def celsius(self):
        """获取当前温度的摄氏值。"""
        return self._celsius

    @celsius.setter
    def celsius(self, value):
        """设置摄氏温度，温度不能低于绝对零度。"""
        if value < -273.15:
            raise ValueError("温度不能低于绝对零度 (-273.15°C)")
        self._celsius = value

    @property
    def fahrenheit(self):
        """通过摄氏温度计算华氏温度。"""
        return self._celsius * 9 / 5 + 32

    @fahrenheit.setter
    def fahrenheit(self, value):
        """通过华氏温度设置摄氏温度。"""
        self.celsius = (value - 32) * 5 / 9

# 使用示例
temp = Temperature(25)  # 初始化时传入摄氏温度
print("摄氏温度:", temp.celsius)        # 输出：25
print("华氏温度:", temp.fahrenheit)       # 输出：77.0

# 修改华氏温度，会自动更新摄氏温度
temp.fahrenheit = 86
print("修改后的摄氏温度:", temp.celsius)   # 输出：30.0

# 修改摄氏温度，setter 内置校验功能
try:
    temp.celsius = -300  # 低于绝对零度，将引发异常
except ValueError as e:
    print("错误:", e)
```

## @functools.lru_cache

缓存函数的结果，以后出现相同参数的调用时，直接返回缓存的结果，不必重新执行函数。

通过参数 `maxsize`，可以灵活控制缓存大小，从而在内存使用和性能之间找到合适的平衡点。

```python
import time
from functools import lru_cache

@lru_cache(maxsize=128)
def fibonacci(n):
    """计算斐波那契数列的第 n 个数字"""
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

def measure_time(n):
    start = time.perf_counter()
    result = fibonacci(n)
    end = time.perf_counter()
    return result, end - start

if __name__ == "__main__":
    n = 35  # 选择一个比较大的数字，能看出性能差异
    result, elapsed = measure_time(n)
    print(f"fibonacci({n}) = {result}，耗时 {elapsed:.6f} 秒")
    
    # 第二次调用同样的参数会直接从缓存返回，极快
    result, elapsed = measure_time(n)
    print(f"重复调用：fibonacci({n}) = {result}，耗时 {elapsed:.6f} 秒")

```

## @functools.wraps

自定义装饰器时，保留原函数的**元数据**，类似**函数名称**和**函数文档**这种。

**不使用functools.wraps**

```python
def my_decorator(func):
    def wrapper(*args, **kwargs):
        print("【装饰器】调用了包装函数。")
        return func(*args, **kwargs)
    return wrapper

@my_decorator
def greet(name):
    """向给定的名字问好。"""
    print(f"Hello, {name}!")

# 调用函数
greet("Alice")

# 查看函数元数据
print("函数名称:", greet.__name__)  # 输出：wrapper
print("函数文档:", greet.__doc__)    # 输出：None

```

**使用functools.wraps**

```python
import functools

def my_decorator(func):
    @functools.wraps(func)  # 使用 functools.wraps 复制元数据
    def wrapper(*args, **kwargs):
        print("【装饰器】调用了包装函数。")
        return func(*args, **kwargs)
    return wrapper

@my_decorator
def greet(name):
    """向给定的名字问好。"""
    print(f"Hello, {name}!")

# 调用函数
greet("Bob")

# 查看函数元数据
print("函数名称:", greet.__name__)  # 输出：greet
print("函数文档:", greet.__doc__)    # 输出：向给定的名字问好。

```

## @abc.abstractmethod

抽象基类，要求子类必须实现被设置为abstractmethod的函数，否则在实例化子类时报错。

```python
from abc import ABC, abstractmethod

class Animal(ABC):
    """
    这是一个抽象基类，定义了动物必须具备的行为接口。
    """

    @abstractmethod
    def make_sound(self):
        """
        抽象方法，所有动物都必须实现发出声音的行为。
        """
        pass

    @abstractmethod
    def move(self):
        """
        抽象方法，所有动物必须实现移动的行为。
        """
        pass

# 若子类没有实现所有抽象方法，则这个子类也会被认为是抽象类，无法实例化
# 例如，如果下面的 Cat 类注释掉某个方法实现，将无法创建 Cat 的实例。

class Cat(Animal):
    def make_sound(self):
        return "Meow!"

    def move(self):
        return "Cat walks gracefully."

if __name__ == "__main__":
    # 尝试实例化 Animal 会报错：
    try:
        generic_animal = Animal()
    except TypeError as e:
        print("错误:", e)

    # 正确实例化具体实现了所有抽象方法的子类 Cat
    kitty = Cat()
    print("Cat 发出的声音:", kitty.make_sound())
    print("Cat 的移动方式:", kitty.move())
```



`@functools.wraps`   在编写自定义装饰器时使用，能够把被装饰函数的名称、文档字符串等元数据复制到新函数上，从而保持其可读性和调试信息。

`@abc.abstractmethod`   来自 `abc` 模块，用于标记基类中的抽象方法，要求所有子类必须为该方法提供具体实现。

`@dataclasses.dataclass`   来自 `dataclasses` 模块，可自动生成 `__init__`、`__repr__`、`__eq__` 等特殊方法，从而简化数据类的定义。

`@contextlib.contextmanager`   将生成器函数转换为上下文管理器，使得定义 with 语句所需的资源管理逻辑更加简洁。

`@functools.singledispatch`   使普通函数实现单分派泛函数，根据第一个参数的类型自动选择合适的函数实现，便于函数重载。

`@functools.total_ordering`   只需在类中定义一种或几种比较方法，此装饰器可自动生成其它比较方法，减少重复代码。

`@functools.cached_property`   （Python 3.8+）用于缓存属性值，即首次调用时计算结果并保存在对象上，后续直接返回缓存值，适用于开销较大的属性计算。

`@typing.overload`   用于类型提示，引入多个函数签名以支持重载，在实际运行时不会对逻辑产生影响，但能帮助静态类型检查工具更好地理解函数接口。

`@pytest.fixture`   在 pytest 测试框架中定义测试夹具，用于在测试前后设置和清理测试环境，非常实用。

`@pytest.mark.parametrize`   也属于 pytest，用于参数化测试函数，使得一个测试可以用多个测试数据运行，提升测试覆盖率和代码清晰度。



# 自定义装饰器

只需要理解2个知识点

**第一个：**语法糖拆解后如下

```python
@my_decorator
def foo():
    pass
```

等价于

```python
def foo():
    pass
foo = my_decorator(foo)
```

**第二个：**函数可以当作参数被传递到另一个函数，函数可以返回一个函数当作返回值

```python
def foo():
    pass
foo = my_decorator(foo)

# my_decorator 函数接收一个参数，且这个参数是一个函数，就是这里的foo函数
# my_decorator 函数返回值是一个函数
# 所以现在 foo 函数变为了 my_decorator 函数的返回值了
```

**例子：**

```python
from typing import Any

# 定义一个自定义装饰器
def my_decorator(func: Any) -> Any:
    def wrapper(*args: Any, **kwargs: Any):
        print(f"在调用原函数之前执行一些代码")
        result = func(*args, **kwargs) # 调用原函数
        print(f"在调用原函数之后执行一些代码")
        return result
    return wrapper

# 使用装饰器语法@my_decorator装饰函数
@my_decorator
def greet(name: str, greeting: str):
    """向某人问好"""
    print(f"{greeting}, {name}!")
    return f"{greeting}, {name}!"

# 调用 gree函数来验证装饰器的效果
if __name__ == "__main__":
    result = greet("Alice", greeting="Hi")
```

# Flusk

