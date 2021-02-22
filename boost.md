链接第三方库：

我们在项目中用到的第三方库需要链接时，一般情况下我们会这样做。首先将库路径告诉编译器，其次告诉编译器库的名字。不管是用makefile或是vs的可视化编辑，都是这个套路。用boost的时候就厉害了。之需要将库路径告诉编译器就行了，不用告诉编译器需要的库名字。为什么呢？归功于（或者说背锅）boost的auto_link机制。

boost根目录下的（就是存放boost头文件的那个文件夹下）有一个config文件夹，config文件夹下有一个auto_link.hpp文件，就TMD是这个文件！秀的一逼！看看它都做了什么伤天害理的事！！！







boost自动链接库auto_link.hpp

使用boost时，不需要在编译器(cmake或vs可视化界面)中指定库名字

```c++
//只需在vs中设置附加库目录就行了
//不需要在链接器->附加依赖项中填写需要的.lib的名字
#include <stdlib.h>
#include <boost/thread.hpp>
int main()
{
	system("pause");
	return 0;
}
```

```c++
#define BOOST_ALL_NO_LIB//告诉boost，别TM自动链接！我不相信你！你个脑残！
#pragma comment (lib, "libboost_thread-vc100-mt-gd-1_54.lib")//告诉编译器，我需要这个库
#pragma comment (lib, "libboost_date_time-vc100-mt-gd-1_54.lib")//告诉编译器，我需要这个库
#pragma comment (lib, "libboost_system-vc100-mt-gd-1_54.lib")//告诉编译器，我需要这个库
#pragma comment (lib, "libboost_chrono-vc100-mt-gd-1_54.lib")//告诉编译器，我需要这个库
#include <stdlib.h>
#include <boost/thread.hpp>
int main()
{
	system("pause");
	return 0;
}
```

