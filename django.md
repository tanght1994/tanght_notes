# 简介

django本质上是一个接收两个参数，返回一个可迭代对象的函数。

```python
def application(environ, start_response):
    # 我们可以从environ中获取一些信息，environ中包含了客户端发送过来的信息
    # 这里就不管environ中的信息了，不管environ是什么，我们都返回123给它

    # status是一个字符串，类似 "200 OK" "404 Not Found"等
    status = "200 OK"
    
    # my_header是一个list，每一个元素是一个tuple，类似("Content-Type", "text/html")
    my_header = [
        ("Content-Type", "text/html"),
        ("Content-Encoding", "gzip"),
        ("Set-Cookie", "xxxxxxxxxx"),
    ]
    
    # 我们需要调用start_response来设置response的header
    start_response(status, my_header)
    
    # 最后返回一个可迭代对象(可以被for调用就行),这个可迭代对象的内容会被合并到一块，当作response的body
    return [b'1', b'2', b'3']
```

运行之后，客户端接收到的内容如下：

```
HTTP/1.1 200 OK
Content-Encoding: gzip
Content-Type: text/html
Set-Cookie: xxxxxxxxxx
Date: Mon, 22 Mar 2021 08:45:43 GMT
Server: WSGIServer/0.2 CPython/3.9.2

123
```

以下内容是我们的函数设置的：

- 200 OK
- Content-Encoding: gzip
- Content-Type: text/html
- Set-Cookie: xxxxxxxxxx
- 123

以下内容是**调用我们的函数的那个程序**添加的：

- HTTP/1.1
- Date: Mon, 22 Mar 2021 08:45:43 GMT
- Server:  WSGIServer/0.2 CPython/3.9.2





创建项目

```shell
# 创建一个HelloWorld项目
django-admin startproject HelloWorld

# 启动网站
python manage.py runserver localhost:8080
```



# ORM源码解析

django/db/models/sql/compiler.py中Class SQLCompiler的def execute_sql是ORM逻辑的最后出口，负责执行SQL语句，在这里打个断点，顺着调用栈往前看就ok了，ORM设计的相当复杂，像一坨屎！



# 自定义异常处理

django异常时(404，权限，用户view函数异常等)，默认返回一个html页面，但是与前端商量好了，不管任何情况，服务端永远返回JSON，这时候怎么办呢？

通过中间件process_exception来处理嘛？对不起，只能处理views异常，(404，权限等异常依然解决不了)，这时候我们就要用绝招了，直接修改django源码，别修改源文件，而是import之后重写几个函数而已。

在`django/core/handlers/exception.py`中存在几个函数，这几个函数控制着django的异常处理：

- convert_exception_to_response：django加载中间件的时候，用这个函数包装了所有中间件函数
- response_for_exception：处理一些细节，没什么卵用
- get_exception_response：通过错误码，找到对应的异常处理函数，并调用，异常处理函数是那些呢？在django/views/defaults.py中有一些，也可以自己写一些
- handle_uncaught_exception：没找到错误处理函数的时候，进入这个函数 

狠一点的话，直接重写response_for_exception，将exception塞进json中返回就可以了

温柔一点的话，仿照get_exception_response，分类处理就好了