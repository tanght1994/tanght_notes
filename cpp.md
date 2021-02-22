# gcc/g++

CPATH：gcc/g++搜索头文件的路径，以:分隔

CPLUS_INCLUDE_PATH：g++搜索头文件的路径，以:分隔

C_INCLUDE_PATH：gcc搜索头文件的路径，以:分隔

LIBRARY_PATH：gcc/g++链接时搜索动态库/静态库的路径，以：分隔

LD_LIBRARY_PATH：程序运行时加载动态库的路径



# char与wchar_t

```c++
#include<stdio.h>
#include<locale.h>
#include<Windows.h>
int main()
{
	wchar_t str[] = L"你好啊";
	setlocale(LC_ALL, "Chs");
	printf("%ls %lc", str, str[1]);
	system("pause");
	return 0;
}

void fun1()
{
    wchar_t str[] = L"你好啊";
	setlocale(LC_ALL, "Chs");
	printf("%ls %lc", str, str[1]);
}

void fun1()
{
    char str[] = "你好啊";
	printf("%s %c", str, str[1]);
}
```



# coredump文件的生成与使用

windows下开启文件崩溃时自动创建dump文件的功能，以管理员身份运行下面的脚本即可。

```bash
@echo off
echo 正在启用Dump...
reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\Windows Error Reporting\LocalDumps"
reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\Windows Error Reporting\LocalDumps" /v DumpFolder /t REG_EXPAND_SZ /d "C:\CrashDump" /f
reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\Windows Error Reporting\LocalDumps" /v DumpType /t REG_DWORD /d 2 /f
reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\Windows Error Reporting\LocalDumps" /v DumpCount /t REG_DWORD /d 10 /f
echo Dump已经启用
pause
@echo on
```

- DumpFolder：告诉windows当程序崩溃时，自动创建的dump文件储存到哪里
- DumpType：告诉windows当程序崩溃时，创建的dump文件的类型，(0，不清楚)(1，只包含关键信息的dump文件)(2，包含全部信息的dump文件)
- DumpCount：告诉windows最大保留Dump个数，默认为10



windows下关闭自动创建dump文件的功能，以管理员身份运行下面的脚本即可。

```bash
@echo off
echo 正在关闭Dump...
reg delete "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\Windows Error Reporting\LocalDumps" /f
echo Dump已经关闭
pause
@echo on
```

windows下dump文件的使用

vs编译项目的时候，除了生成一个.exe文件，还会生成一个对应的.pdb文件，pdb文件是调试用的，pdb文件包含了编译后程序指向源代码的位置信息，用于调试的时候定位到源代码。

1. 123.exe崩溃了
2. 操作系统发现123.exe崩溃时，会自动保存当前的123.exe的内部信息，调用栈之类的信息，这个信息保存到一个名为123xxx.dump的文件中，放到你设置的目录中，例如C:\crashdump文件夹下
3. 找到123.exe对应的,pdb文件，编译123.exe的时候自动生成了对应的.pdb文件
4. 把123.exe与123.pdb与123xxx.dump放到同一个文件夹下
5. 双击123xxx.dump，vs自动启动
6. 点击仅限本机调试
7. vs自动跳转到程序崩溃时的位置，甚至可以看一下调用找信息



# openssl

```c++
//VC++目录->包含目录，添加你的openssl库的头文件目录
//链接器->输入->附加依赖项，添加libcrypto.lib
//运行程序时会报错说缺少xxx.dll
//去openssl安装的目录找到这个xxx.dll文件，复制到项目的Debug文件夹下
//ok了

#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>
#include <string.h>
#include <openssl/evp.h>

int main()
{
	do
	{
		//我们将要对msg1和msg2这两块数据做摘要运算
		char msg1[] = "Hello Dog\n";
		char msg2[] = "Hello Cat";
		
		//md中储存了将要使用的摘要算法标识，有很多摘要算法，你得告诉opssl用什么算法进行摘要运算啊！
		//EVP_get_digestbyname("SHA1")返回sha1算法的标识，储存到md中
		//接下来将md传给摘要运算函数，然后那个函数就知道了，你想要用sha1进行运算
		const EVP_MD *md = nullptr;
		md = EVP_get_digestbyname("SHA1");	//md = EVP_sha1();效果一样
		if (md == NULL) {
			printf("Fuck! Don't Find Your DigestName");
			break;
		}

		//mdctx为程序上下文，其实就是一堆参数，包裹成了一个结构体，比直接传一堆参数方便。
		//比如EVP_DigestInit_ex()这个函数需要100个参数，
		//你不能真的设计成void EVP_DigestInit_ex（arg1, arg2, arg3, arg4...）写100个参数吧！
		//所以将这些参数放到EVP_MD_CTX结构体中，直接传一个EVP_MD_CTX就好了。
		//其实EVP_MD_CTX里面就是一堆int,double,char*等等的基本数据结构。
		EVP_MD_CTX *mdctx = nullptr;
		mdctx = EVP_MD_CTX_new();//创建一个程序上下文

		//初始化程序上下文
		//md中储存了你想要用的摘要算法，这个函数用md去初始化mdctx
		//所以mdctx就知道了你想要用什么算法了，并且mdctx还包含了其它信息供后面的函数用
		EVP_DigestInit_ex(mdctx, md, NULL);

		//向算法添加数据，将msg1添加进去
		EVP_DigestUpdate(mdctx, msg1, strlen(msg1));
		
		//向算法添加数据，将msg2添加进去
		EVP_DigestUpdate(mdctx, msg2, strlen(msg2));

		//如果有数据还可以继续添加，我们这里没有了，到这里就结束了
		//EVP_DigestUpdate(mdctx, msgN, strlen(msgN));

		//告诉openssl，我已经添加完数据了，可以给我计算摘要值了
		unsigned char md_value[EVP_MAX_MD_SIZE];	//储存最终的摘要值
		unsigned int md_len;						//储存摘要值的长度
		EVP_DigestFinal_ex(mdctx, md_value, &md_len);
		
		//释放上下文，将这一堆参数free掉
		EVP_MD_CTX_free(mdctx);

		//打印摘要值到屏幕上
		printf("Digest is: ");
		for (int i = 0; i < md_len; i++)
		{
			printf("%02x", md_value[i]);
		}			
		printf("\n");

	} while (false);

	system("pause");
	return 0;
}
```





# allocator与new的比较

new一个东西时，既申请了内存，又在申请的这块内存中进行了初始化（对元素调用默认构造函数）。

allocator一个东西时，只申请内存，不进行初始化。比new少了一步，所以比new快。

```c++
#include <iostream>
#include <vector>
#include <string>
#include <Windows.h>

#define gNumber 1000000

int main()
{
	unsigned long uStartTime = 0;
	unsigned long uEndTime = 0;

	//用new申请gNumber个字符串的空间，new会为每个字符串调用一次默认构造函数
	uStartTime = GetTickCount();
	std::string *pStr1 = new std::string[gNumber];
	uEndTime = GetTickCount();
	std::cout << "new cost: " << uEndTime - uStartTime << "ms" << std::endl;
	delete[] pStr1;


	//用allocator申请gNumber个字符串的空间，allocator不会调用字符串的默认构造函数
	uStartTime = GetTickCount();
	std::allocator<std::string> allocateStr;
	std::string *pStr2 = allocateStr.allocate(gNumber);
	uEndTime = GetTickCount();
	std::cout << "allocator cost: " << uEndTime - uStartTime << "ms" << std::endl;

	for (size_t i = 0; i < gNumber; ++i)
	{
		//如果前面构造了每个字符串，需要在这里析构每个字符串，不然会内存泄漏
		//前面没有构造，所以这里不用析构
	}
	allocateStr.deallocate(pStr2, gNumber);

	system("pause");
	return 0;
}
```

![image-20200412013556703](assets/image-20200412013556703.png)

```c++
#include <iostream>
#include <Windows.h>

#define gNumber 1

class CA
{
public:
	CA(){ std::cout << "构造函数" << std::endl; }
	~CA() { std::cout << "析构函数" << std::endl; }
};

int main()
{
	std::cout << "start new..." << std::endl;
	CA * p1 = new CA[gNumber];
	delete[] p1;

	std::cout << "start allocator..." << std::endl;
	std::allocator<CA> allocatorCA;
	CA *p2 = allocatorCA.allocate(gNumber);
	allocatorCA.deallocate(p2, gNumber);

	system("pause");
	return 0;
}
```

![image-20200412013446672](assets/image-20200412013446672.png)



# mysql

MySQL查询结果集：MYSQL_RES

![image-20200421174358380](assets/image-20200421174358380.png)

```sql
SELECT * FROM table1;
```

我们的程序运行完尚书查询语句之后，mysql如何将这5条记录发送给我们？难道直接发过来一张excel表格么？肯定不是的，可以假设它发过来的是一堆字符串，其实就是一堆字符串，只不过是mysql自定义的格式的字符串。那么OK，我们如何解析这堆字符串？从第几个字节到第几个字节是第一条记录？第二条记录又记录在这堆字符串的什么地方？第3条呢？

OK，假设我们能找到第N条记录的位置，那么我们又如何找到第一条记录的哪几个字节表示第一个字段？第二个字段？第三个字段？

OK，太麻烦了！还好开发mysql的公司已经帮我们写好了，我们只需要用他的API就好了。



```c++
//执行sql语句，正常返回0
int mysql_query(MYSQL *mysql, const char *stmt_str);

//如果上一次执行的sql语句有结果集，则取结果集
//如果上次执行了MultipleStatement，可以多次调用此函数，每次取一条语句的结果集，没有结果集可取了则返回NULL，并且mysql_field_count()为0
MYSQL_RES *mysql_store_result(MYSQL *mysql);

// more results? -1 = no, >0 = error, 0 = yes 
int mysql_next_result(MYSQL *mysql);

//释放结果集
void mysql_free_result(MYSQL_RES *result)


```



# 代码中制定库名

```c++
#pragma comment (lib,"xxx.lib")
```





# 动态库的制作与使用

### 动态库是什么

动态库就是一堆函数的打包，调用这个动态的库的应用程序可以直接使用这个库中的函数，它是二进制格式的，不是源代码。例如有这么一个函数，函数名字叫fun1，它接收两个参数a和b，经过一系列骚操作之后返回结果c，你不需要清楚骚操作是什么，总之骚操作就是非常复杂的逻辑运算，代码实现的话要100w行。这个函数很好用，以至于你写的很多程序中都需要用到这个函数，甚至其他程序员（国内外的程序呀，火星的程序员，哈雷彗星上的程序员）也需要这个函数。

这时候有最直观的方法是，将fun1的代码复制N份发给各个程序员，其他程序员将fun1的代码放到自己的项目中，编译。但是这种方法很low啊，而且不方便，这代码有100w行啊，由很多文件组成，每次都复制代码的话太不方便了。更何况，开发这个fun1函数的程序员，并不想让其它的程序员知道这个函数的具体代码是怎么写的（因为这个代码写的炒鸡烂，他的作者不好意思被别人知道）。所以动态库（静态库也一样，这里不讨论静态库，动态库的区别，google上一堆解释，自己去查）就出现了，这个程序员将fun1编译成动态库，发给其它人，同时将动态库的说明书（也就是.h文件喽）也发给其他程序员。他是怎么做的呢？

1. 将fun1的源代码编译成动态库abc.dll、abc.lib（Windows，Linux中有些许的区别）。
2. 将fun1的头文件（函数声明，你总得告诉其它程序员这个函数接收几个参数，返回什么类型吧？不然其它程序员怎么调用你这个函数啊）与abc.dll与abc.lib发送给其它人。
3. 其他人有了这个函数的声明，就可以在代码中调用了。有了.lib，就可以编译了。有了.dll就可以运行了。

**注：.lib .dll是什么一会再说**

所以最终，你要知道，动态库就是一堆函数的实现过程，打包成一个.dll而已。一个动态库中可以包含很多函数的。

### Windows平台

#### 动态库的制作

使用VisualStudio2017制作动态库，最终生成MyFirstDll.dll与MyFirstDll.lib。我们将要制作的MyFirstDll库中包含了四个函数，分别是加减乘除，函数声明如下：

```c++
double ThtAdd(const double &a, const double &b); //计算a + b
double ThtSub(const double &a, const double &b); //计算a - b
double ThtMul(const double &a, const double &b); //计算a * b
double ThtDiv(const double &a, const double &b); //计算a / b
```

我们要在TestDll.exe中调用MyFirstDll.dll中的四个函数，测试是否成功。

1.打开VS，新建DLL项目，建完之后先编译一下，测试是否能编译成功，如果新建的项目都不能编译成功，把证明你的环境配置有问题，自己解决。99.9999%的情况下肯定能成功。

![image-20200321174812977](assets/image-20200321174812977.png)

2.新建两个文件[ThtCalculation.h、ThtCalculation.cpp]

![image-20200321180002892](assets/image-20200321180002892.png)

3.在ThtCalculation.h添加四个函数的声明。__declspec(dllexport)是必须的，作用是告诉编译器，这个函数可以给外部使用。不加declspec(dllexport)的话，外部软件就不能调用这个函数了。咱们的四个函数全部是给外部调用的，所以全部加上。

![image-20200321182545507](assets/image-20200321182545507.png)

```c++
//ThtCalculation.h
#pragma once
__declspec(dllexport) double ThtAdd(const double &a, const double &b);
__declspec(dllexport) double ThtSub(const double &a, const double &b);
__declspec(dllexport) double ThtMul(const double &a, const double &b);
__declspec(dllexport) double ThtDiv(const double &a, const double &b);
```

4.在ThtCalculation.cpp中实现这四个函数。"pch.h"是windows快速编译的文件，没有这个文件的话也可以不include它。

![image-20200321184106421](assets/image-20200321184106421.png)

```c++
//ThtCalculation.cpp
#include"pch.h"
#include<cmath>
#include"ThtCalculation.h"

double ThtAdd(const double & a, const double & b)
{
	return a + b;
}

double ThtSub(const double & a, const double & b)
{
	return a - b;
}

double ThtMul(const double & a, const double & b)
{
	return a * b;
}

double ThtDiv(const double & a, const double & b)
{
	if (abs(b) < 0.000001)
	{
		return 0.0;
	}
	return a / b;
}

```

5.编译

![image-20200321184545665](assets/image-20200321184545665.png)

6.找到编译完的动态库

![image-20200321184724351](assets/image-20200321184724351.png)

![image-20200321185019114](assets/image-20200321185019114.png)

![image-20200321185211507](assets/image-20200321185211507.png)

![image-20200321185529662](assets/image-20200321185529662.png)

7.将动态库和.h文件放到同一个文件夹中，结束。

![image-20200321222342395](assets/image-20200321222342395.png)

#### 动态库的使用

我们制作完了动态库，最终包含上述三个文件，一个.dll一个.lib一个.h。我们如何使用呢？很简单，直接将.h包含到项目中，调用动态库中的函数就行了。

1.创建TestDll项目

![image-20200321222841759](assets/image-20200321222841759.png)

2.将动态库中的.h复制到我们的项目文件夹中，并添加到项目中

![image-20200321223048932](assets/image-20200321223048932.png)

3.创建main函数，调用动态库中的函数

![image-20200321223234071](assets/image-20200321223234071.png)

```c++
//main.cpp
#include<iostream>
#include<Windows.h>
#include"ThtCalculation.h"
using namespace std;

int main()
{
	cout << ThtAdd(10, 20) << endl;
	cout << ThtSub(10, 20) << endl;
	cout << ThtMul(10, 20) << endl;
	cout << ThtDiv(10, 20) << endl;
	system("pause");
	return 0;
}
```

4.告诉编译器，.lib的名字是什么，我们这里叫做MyFirstDll.lib。

![image-20200321223932071](assets/image-20200321223932071.png)

![image-20200321224117725](assets/image-20200321224117725.png)

![image-20200321224401213](assets/image-20200321224401213.png)

5.告诉编译器，去哪里找到我们的动态库。编译器默认在项目的源文件目录搜索我们的.lib，如果你将.lib复制到项目的源代码目录中的话，那就不需要告诉编译器去哪里找动态库了。我们这里将.lib放在其它地方，所以我需要告诉编译器去哪里找.lib。

![image-20200321225217477](assets/image-20200321225217477.png)

![image-20200321225342744](assets/image-20200321225342744.png)

6.编译成TestDll.exe

![image-20200321225559188](assets/image-20200321225559188.png)

![image-20200321225801281](assets/image-20200321225801281.png)

7.双击运行我们的TestDll.exe，不出意外，肯定会报错，说找不到MyFirstDll.dll

![image-20200321225940706](assets/image-20200321225940706.png)

8.终于.dll文件派上用场了，细心的你一定发现了，前面那么多步骤，都没有用到.dll。你的TestDll.exe会从它自己所在的目录和你的PATH环境变量所配置的路径中去找MyFirstDll.dll找不到就报错。我们这里就报错了，解决办法有多种：

1. 将MyFirstDll.dll所在的文件夹设置到PATH环境变量中
2. 将MyFirstDll.dll复制到TestDll.exe的文件夹中
3. 将MyFirstDll.dll复制到已经是PATH环境变量的文件夹中

我们这里用最简单的办法，直接把MyFirstDll.dll和TestDll.exe放到相同的文件夹中，再次运行TestDll.exe。成功！

![image-20200321230839660](assets/image-20200321230839660.png)

![image-20200321230923258](assets/image-20200321230923258.png)

注：.lib用于编译，.dll用于运行



### Linux平台

Linux平台特简单，这里就不说了。任何事情Windows总是要麻烦一些。

