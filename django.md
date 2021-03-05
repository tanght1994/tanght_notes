# 简介

django本质上是一个接收两个参数，返回一个可迭代对象的函数



创建项目

```shell
# 创建一个HelloWorld项目
django-admin startproject HelloWorld

# 启动网站
python manage.py runserver localhost:8080
```



setting.py

```shell
# 设置静态资源在url中的前缀，访问静态资源时，url需加上STATIC_URL这个前缀
STATIC_URL = '/static/'

# 在html模板中使用外部css或其他资源，如<link rel="stylesheet" href="static/haha.css"/>时，django去哪里找static/haha.css？
# 设置静态资源绝对路径
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)
```



创建项目

创建template目录

创建static目录

配置setting.py

模板路径

静态资源前缀

静态资源路径

配置urls.py



注释掉

```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',  # 注释掉
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
```



```python
# render 读取模板转换成字节流
from django.shortcuts import render

# HttpResponse 将字符串转换成字节流
from django.http import HttpResponse


def fun(request):
    request.method  # 方法名  "GET" or "POST"
    request.GET  # GET中的数据
    request.POST # POST中的数据部分
    
    return redirect('URL') # 重定向到URL这个网页
	return render(request, '模板路径', {'渲染内容对象'})
	return HttpResponse('字符串或者字节')

```



模板语句

```python
{{ msg }}  # msg占位符
{{ msg.0 }}  # msg是个列表，取第0个元素

# for循环
{% for i in result %}
	{{ i }}
{% endfor %}

# if语句
{% if 1 > 2%}
	语句
{% endif %}
```



Ajax(jquery)

```js
$.ajax({
    url: "/test/",
    type: "POST",
    data: {数据字典},
    dataType: "JSON", 	//设置arg类型
    success: function(arg){
        //arg时字符串格式
        //如果是JSON,可以用JS的JSON函数将arg变成对象了
    }
})

//页面加载完毕后，开始执行
$(function(){
   // 开始写 jQuery 代码...
});
```



js阻止默认事件的发生

```html
//给标签添加个我们自己的事件，return我们我自的函数，如果我们自己的函数返回false，则不执行默认事件
<a href="www.baidu.com" onclick="return myfun()">123</a>
<script>
    function myfun(){
        return false; //防止a标签的默认跳转行为
    }
</script>
```



html

```html
# 前端跳转
location.href="/test/"  //跳转到/test/
location.reload()  //刷新当前页面
```



母版

```django
//Base.html中
{% block content %}
{% endblock %}

{% block css %}
{% endblock %}

{% block js %}
{% endblock %}


//123.html中
{% extends 'Base.html' %}
{% block content %}
balabala		//用这些东西替换母版中的block content段
{% endblock %}

{% block js %}
balabala		//用这些东西替换母版中的block js
{% endblock %}

{% block css %}
balabala		//用这些东西替换母版中的block css
{% endblock %}
```



cookie

```
request.COOKIES.get('k1')
request.get_signed_cookie('k1', 'salt')


obj = render(...)
obj.set_cookie(k1, v1, max_age, path)
obj.set_signed_cookie(k1, v1, max_age, path, 'salt')
```



```
(?P<a1>\w+)  \w+匹配到的东西，传递给a1参数
```



```
import url, include

url(r'^app01/', include('app01.urls'))	//匹配到app01/的时候，剩下的url交给app01.urls去匹配

url(r'^app01/', include('app01.urls'))	//url匹配失败时，执行default_fun函数
```



多个app

```
python manag.py startapp app01
```



```python
# 反向生成url
# 可用于模板中 {% url 'url函数映射名n1' %}
url(r'^index/', views.index, name='n1')

from .... import reverse
def index(request):
    url = reverse('n1')
    print(url) # /index/
    

url(r'^index/(\d+)', views.index, name='n1')

from .... import reverse
def index(request, a):
    url = reverse('n1', args=(123,))
    print(url) # /index/123

```



ORM

```shell
python manage.py makemigrations
python3 manage.py migrate

#[obj,obj,obj,obj,]
models.UserInfo.objects.all()

#[dict,dict,dict,dict,]
models.UserInfo.objects.all().values('id', 'name')

#[dict,dict,dict,dict,]
models.UserInfo.objects.all().values('id', 'name')

#[tuple,tuple,tuple,]
models.UserInfo.objects.all().values_list('id', 'name')
```



app01中可以创建一个views模块，views中写多个函数文件，这样就可以对views进行细分了





urls

```python
# 路由分发
# 将app01/的内容，交给app01.urls
urlpatterns = [
    path('app01/', include('app01.urls')),
    path('^', default), # 匹配失败时，执行default函数
]



# 正则表达式
# '^index.html$'    ^为开始符，$为终止符
def test(request, arg):
    pass

# 'test/(\w+)/'
# url中写正则表达式，可以将匹配到的数据，以函数参数的形式传递给函数
# 这里将(\w+)的内容传递给arg参数
def test(request, arg):
    pass

# 'test/(\w+)/(\w+)/'
# 匹配两块数据的话，就用两个参数来接收，按顺序传递给a1,a2
def test(request, a1, a2):
    # arg1匹配第一个(\w+)
    # atg2匹配第二个(\w+)
    pass

# 'test/(?P<a1>\w+)/(?P<a2>\w+)/'
# ?P<x>可以在url中指定匹配到的数据传递给函数的哪个函数
# (?P<a1>\w+)不管这块数据在哪个位置，都将传递给函数的a1参数
def test(req, a1, a2):
    pass

# 'test/(?P<a1>\w+)/(?P<a2>\w+)/'  ok,kwargs中可以找到s1, a2
# 'test/(\w+)/(\w+)/'  ok,args按顺序接收url中匹配到的数据
# 也就是说，这个函数支持以上两种url
# 不支持两种形式混写的url，例如： 'test/(\w+)/(?P<a1>\w+)/'
def test(req, *args, **kwargs):
    pass



# url命名
urlpatterns = [
    path('^haha/(\w).html$', views.fun, name='n1'),
]

from django.urls import reverse
def test(req, a1):
    a = reverse('n1', args=('123'))
    print(a)  #a为'haha/123.html'
    
# ^haha/(\w).html$'
a = reverse('name', args=('123',))

# ^haha/(?P<a1>\w).html$'
a = reverse('name', kwargs={'a1': '123'})

#html中应用url命名  django将找到urlname然后填充到html中的{% url "urlname" %}中
#比如urlname为  'abc/login.html'   则action='abc/login.html'
<form method="POST" action="{% url "urlname" %}">

#name为'/edit/(\w+)' 将i添加到第一个位置中，有2，3，4个正则位置是一样的
{% for i in user_list %}
	<li>{{ i }} | <a href="/edit/{{ i }}/">编辑</li>
    <li>{{ i }} | <a href="{{ url "name" i}}">编辑</li>
{% endfor %}
```



分页

```python
from django.core.paginator import Paginator, Page

def test(req):
    user_list = models.UserInfo.objects.all()
    # arg1是个object_list
    # arg2是每页显示几条数据
    paginator = Paginator(user_list, 10)
    # page代表第一页,page中有个object_list属性，是第一页中的所有数据
    page = paginator.page(1)
    
    
# html中执行python对象的函数，需要加上|safe
# 是python_obj.fun而不是python_obj.fun()，不用加()
<a href="{{ python_obj.fun|safe }}">上一页</a>
    
```



csrf

```python
# html中设置一个隐藏的csrf随机数，提交表单的时候连同随机数一起提交

# ajax中也可以提交csrf随机数，可以在header中也可以在post body中
```



xss

```python
# 1.在html模板中加|safe
# 2.在views函数中加mark_safe装饰器
# 3.在views类中加装饰器
```



session

```
保存在服务器的键值对，sessionid发送给浏览器的cookies

```



From表单验证

```python
#创建一个类
class FromTest(From):
    user = fields.CharField(....)
    pwd = fields.CharField(....)
    
def test(req):
    obj = FromTest(req.POST)
    result = obj.is_valied()
    return render(req, {"obj": obj})

{% csrf_token %}
<input type="password" name="pwd"/>{{ obj.errors.pwd.0 }}

$.ajax({
    url = 'haha/',
    type = 'POST',
    data = $('#from1').serialize(), #将from1表单中的数据全部打包，包括csrf_token，省的写字典了
})
```



# ORM源码解析

django/db/models/sql/compiler.py中Class SQLCompiler的def execute_sql是ORM逻辑的最后出口，负责执行SQL语句，在这里打个断点，顺着调用栈往前看就ok了，ORM设计的相当复杂，像一坨屎！