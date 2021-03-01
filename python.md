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
# 如果haha是个文件，则加载haha.py，如果没有haha,py则报错
# 如果haha是个目录，则加载haha目录下的__init__.py文件，如果没有__init__.py文件则报错
m = import_module('zhangsan.lisi.wangwu.haha')
```









# Python虚拟环境

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

原理：

定义了——enter——（）与——exit——（）函数的类，可以使用with语句，进入with作用域之前会执行——enter——（）函数，离开with作用于之时会调用——exit——（）函数，不管with代码块中用户写的代码出现什么异常，离开with代码块时，都会执行——exit——（）函数。

```python
with expression as var:
    # 一些代码
```

- 首先执行expression，且expression必须返回一个对象
- expression返回的对象必须带有——enter——（）与——exit——（）方法
- 执行expression返回的对象的——enter——（）方法
- ——enter——（）方法返回的内容赋值给var
- 执行with作用域中用户写的代码
- 离开with作用域，并执行——exit——（）方法
- 注：enter与exit是双下划线，我这个编辑器不能用双下划线，破折号代替了





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
pip install abc_name -i http://mirrors.aliyun.com/pypi/simple/
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



