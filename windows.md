### windows时间相关API

时间相关结构体

```c++
//SYSTEMTIME
typedef struct _SYSTEMTIME {
  WORD wYear;		//年（1601年至30827年）
  WORD wMonth;		//月（1-12）
  WORD wDayOfWeek;	//星期中的第几天（0-6）0为星期日，6为星期六
  WORD wDay;		//一个月中的第几天（1-31）
  WORD wHour;		//小时（0-23）
  WORD wMinute;		//分钟（0-59）
  WORD wSecond;		//秒（0-59）
  WORD wMilliseconds;	//毫秒
} SYSTEMTIME, *PSYSTEMTIME, *LPSYSTEMTIME;

//FILETIME  用两个32位类型拼成一个64位类型，最终的64位单位为纳秒
typedef struct _FILETIME {
  DWORD dwLowDateTime;		//低位
  DWORD dwHighDateTime;		//高位
} FILETIME, *PFILETIME, *LPFILETIME;

//将FILETIME拼成一个64位类型（这可不是Windows函数啊！这是我自己写的，见笑了）
//最终的64位结果单位是100纳秒，也就是说每经过1秒，FileTime增加10,000,000
UINT64 FileTimeToUINT64(const FILETIME& ft)
{
	UINT64 result;
	*((DWORD*)&result) = ft.dwLowDateTime;		 //result的[0-31]位存放FILETIME的LowDate
	*(((DWORD*)&result) + 1) = ft.dwHighDateTime;//result的[32-63]位存放FILETIME的HighDate
	return result;
}
```



```c++
//获取SystemTime类型的时间
void GetLocalTime(LPSYSTEMTIME lpSystemTime);//获取本地时间，在北京就是北京时间，在伦敦就是伦敦时间
void GetSystemTime(LPSYSTEMTIME lpSystemTime);//获取UTC时间，全球一样


//获取FILETIME类型的时间，从1601年1月1日开始所经过的纳秒
void GetSystemTimeAsFileTime(LPFILETIME lpFileTime);//获取UTC时间，储存在FILETIME结构体中，FILETIME高低位可以合成一个64位的数据，单位为100纳秒


//FILETIME---SYSTEMTIME相互转换
BOOL FileTimeToSystemTime(const FILETIME *lpFileTime, LPSYSTEMTIME lpSystemTime);
BOOL SystemTimeToFileTime(const SYSTEMTIME *lpSystemTime, LPFILETIME lpFileTime);


//获取开机经历时间
DWORD GetTickCount();//电脑上次开机到现在，所经历的时间(毫秒)。最多40多天就归零了,因为DWORD空间不够了
ULONGLING GetTickCount64();//电脑上次开机到现在，所经历的时间(毫秒)。一直开机到电脑报废也没问题。


//c语言获取UNIX时间戳，1970年1月1日开始所经过的秒数
time_t CurrentTime = time(nullptr);	//c语言标准库函数，UNIX时间戳复制给CurrentTime
time(&CurrentTime);	//直接将UNIX时间戳赋值给CurrentTime
```



### Windows服务相关

```bash
cmd -install -serviceName "abc"		# 将这条cmd命令注册为win服务，设置这个服务的真实名称为abc
sc delete abc						# 将abc从win服务中删除
net start abc						# 启动abc服务
net stop abc						# 停止abc服务
```

使用nssm工具将普通的exe程序注册为widows服务
