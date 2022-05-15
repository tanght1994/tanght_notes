# 声明

`=`是赋值操作，不是声明变量的操作

`:=`是声明变量的操作

```go
var a string = "test"  //两部操作声明a，再对a赋值 1.var a string   2.a = "test"  
b := "test" // 就一步操作，声明b并初始化为test
```



第二行的`:=`，对于err是赋值操作，out是声明+初始化操作。

```Go
in, err := os.Open(infile)
out, err := os.Create(outfile)
```



`:=`左边至少有一个变量是新变量，否则会报错

```go
in, err := os.Open(infile1)
in, err := os.Open(infile2) // 错误，in和err都是已经存在的变量了
```

# 字符串

rune：是int64类型，可以保存一个unicode码(注意不是utf-8编码)。

ascii码是什么？

对`abcd...123...符号等...`进行排号，比如0号代表字符`a`，1号代表字符`b`。一共128个排号，代表128个字符。所以用一个字节(8位)就能储存一个ascii字符。

unicode码是什么？

对`abcd...123...符号...汉字...日语...各种人类字...火星字...`进行排号

```go
func main() {
	//go中string的底层结构是字节数组[]byte，编码格式为utf-8，所以"a唐b"这个字符串在go底层是这样表示的
	//二进制：                                            十进制：                 十六进制：
	//{01100001, 11100101, 10010100, 10010000, 01100010} {97, 229, 148, 144, 98} {0x61, 0xE5, 0x94, 0x90, 0x62}
	// |--a---|  |------------唐------------|  |---b---|
	//可以看出有些字符占1个元素(a)，有些字符占3个元素(唐)
	s := "a唐b"
	fmt.Printf("%d %d %d %d %d\n", s[0], s[1], s[2], s[3], s[4])

	//rune是int64，可以储存一个很大的数字
	//[]rune(s)会将字符串(字节数组、字节流)按照utf-8格式解码为unicode标号
	//本来"唐"这个字符要占用3个byte元素，现在转为rune之后，只需要占用1个rune(int64)元素
	//[]rune实现了每个元素代表1个字符的愿望
	r := []rune(s)
	fmt.Printf("%d %d %d\n", r[0], r[1], r[2])

	//string()函数可以将rune元素按照utf-8格式编码为[]byte(字节流)
	s1 := string(r)
	fmt.Printf("%d %d %d %d %d\n", s1[0], s1[1], s1[2], s1[3], s1[4])
}
```

重点理解：unicode码与utf-8编码之间的关系

rune代表的是unicode码



# go mod

123



# package与import

import()后面跟的永远是路径，与package name无关

代码中使package的时候，永远是通过package name来使用，与文件夹名字无关

例子，目录结构如下：

```go
test
├── hahapack
│   └── a.go
└── main.go
```



```go
// test/hahapack/a.go
// 虽然我的文件夹的名字是hahapack，但是我的package名字却是xixipack，我乐意！
package xixipack
var A int = 11111
```



```go
// test/main.go
package main

import (
	"fmt"
	xixipack "test/hahapack"  // 引用的时候要用文件夹的名字
)

func main() {
    // 使用的时候要用package的名字
    // 虽然文件夹叫做hahapack，但是包名却是xixipack
    // 所以这里必须要用package name来调用
    // 除非import的重命名
	fmt.Println(xixipack.A)
}

```



# package名字重复了？

import的时候可以重命名，重命名之后就可以使用了，不存在冲突



# Slice

```go
```



# 常用函数

```go
// dst与src是slice类型，并且其中的元素类型必须相同
// dst=[]byte and src=[]int 会报错，编译报错
// src可以使字符串(因为字符串底层也是[]byte)
copy(dst, src)
```







```go
type Request struct {
	Method string  		//POST GET DELETE
	URL *url.URL
	Proto      string 	// "HTTP/1.0"
	ProtoMajor int    	// 1
	ProtoMinor int    	// 0
	Header Header		// map[string][]string
	Body io.ReadCloser
	GetBody func() (io.ReadCloser, error)
	ContentLength int64
	TransferEncoding []string
	Close bool
	Host string
	Form url.Values
	PostForm url.Values
	MultipartForm *multipart.Form
	Trailer Header
	RemoteAddr string
	RequestURI string
	TLS *tls.ConnectionState
	Cancel <-chan struct{}
	Response *Response
	ctx context.Context
}
```





```go
type response struct {
	conn             *conn
	req              *Request // request for this response
	reqBody          io.ReadCloser
	cancelCtx        context.CancelFunc // when ServeHTTP exits
	wroteHeader      bool               // reply header has been (logically) written
	wroteContinue    bool               // 100 Continue协议，分部上传post数据，没什么用
    wants10KeepAlive bool               // Connection: "keep-alive"
	wantsClose       bool               // Connection: "close"
	canWriteContinue atomicBool			// 100 Continue协议，分部上传post数据，没什么用
	writeContinueMu  sync.Mutex			// 100 Continue协议，分部上传post数据，没什么用
	w  *bufio.Writer 	// 底层是cw
	cw chunkWriter		// cw是w的底层,cw的Write会调用conn.bufw
	handlerHeader Header
	calledHeader  bool // handler accessed handlerHeader via Header
	written       int64 // number of bytes written in body
	contentLength int64 // explicitly-declared Content-Length; or -1
	status        int   // status code passed to WriteHeader
	closeAfterReply bool
	requestBodyLimitHit bool
	trailers []string
	handlerDone atomicBool // set true when the handler exits
	dateBuf   [len(TimeFormat)]byte
	clenBuf   [10]byte
	statusBuf [3]byte
	closeNotifyCh  chan bool
	didCloseNotify int32 // atomic (only 0->1 winner should send)
}
```



```go
type conn struct {
	// server is the server on which the connection arrived.
	// Immutable; never nil.
	server *Server

	// cancelCtx cancels the connection-level context.
	cancelCtx context.CancelFunc

	// rwc is the underlying network connection.
	// This is never wrapped by other types and is the value given out
	// to CloseNotifier callers. It is usually of type *net.TCPConn or
	// *tls.Conn.
	rwc net.Conn

	// remoteAddr is rwc.RemoteAddr().String(). It is not populated synchronously
	// inside the Listener's Accept goroutine, as some implementations block.
	// It is populated immediately inside the (*conn).serve goroutine.
	// This is the value of a Handler's (*Request).RemoteAddr.
	remoteAddr string

	// tlsState is the TLS connection state when using TLS.
	// nil means not TLS.
	tlsState *tls.ConnectionState

	// werr is set to the first write error to rwc.
	// It is set via checkConnErrorWriter{w}, where bufw writes.
	werr error

	// r is bufr's read source. It's a wrapper around rwc that provides
	// io.LimitedReader-style limiting (while reading request headers)
	// and functionality to support CloseNotifier. See *connReader docs.
	r *connReader

	// bufr reads from r.
	bufr *bufio.Reader

	// bufw writes to checkConnErrorWriter{c}, which populates werr on error.
    bufw *bufio.Writer	// checkConnErrorWriter中调用,rwc.Write，也就是net.TCPConn的Write

	// lastMethod is the method of the most recent request
	// on this connection, if any.
	lastMethod string

	curReq atomic.Value // of *response (which has a Request in it)

	curState struct{ atomic uint64 } // packed (unixtime<<8|uint8(ConnState))

	// mu guards hijackedv
	mu sync.Mutex

	// hijackedv is whether this connection has been hijacked
	// by a Handler with the Hijacker interface.
	// It is guarded by mu.
	hijackedv bool
}
```







```go
type response struct {
	conn             *conn
    
	w  *bufio.Writer 	// 底层是cw
    
	cw chunkWriter		// cw是w的底层,cw的Write会调用conn.bufw
}

type conn struct {
	server *Server
    
	rwc net.Conn
    
    bufw *bufio.Writer	// checkConnErrorWriter中调用,rwc.Write，也就是net.TCPConn的Write
}
```





```go
go get -u github.com/kataras/iris/v12@latest
```





# proto

编写proto文件，与C++不同的是，golang的proto文件需要在文件中设置option go_package

```shell
option go_package = "{path};{package_name}";
# path：指定生成的xx.pb.go文件的位置(以cmd中--go_out=的路径为基路径)
# package_name：指定xx.pb.go文件中，package的名字
# 下面是具体的例子，生成的文件在当前目录下，文件中的package名字是hahaha
option go_package = "./;hahaha";
# 注意"./;hahaha"最终的路径要加上cmd中指定的--go_out的路径
```

proto文件

```protobuf
syntax = "proto3";

// golang中必须指定这个玩意儿！真他妈的蠢！
option go_package = "./;hahaha";

// package在golang中有TMD什么用？
package test;

enum PhoneType {
    HOME = 0;
    WORK = 1;
}

message Phone {
    PhoneType type = 1;
    string number = 2;
}

message Person {
    int32 id = 1;
    string name = 2;
    repeated Phone phones = 3;
}

message ContactBook {
    repeated Person persons = 1;
}
```

两个可执行程序：protoc，protoc-gen-go

执行`protoc --go_out=. *.proto`，生成xx.pb.go文件

--go_out=plugins=grpc:aaaa   在./aaaa/下生成go文件

protoc --go_out=plugins=grpc,paths=source_relative:. xxxx.proto

protoc --go_out=plugins=grpc:. xxxx.proto

```go
import google.golang.org/protobuf/proto"

// 制作一个protobuf中的结构体
p = &pba.Person{Name: "", .......}
// 将p编码为[]byte
b, e := proto.Marshal(p)
fmt.Println(b)

// 创建一个空的Persion，准备接收解码的数据
p2 := &pba.Person{}
// 将字节流解码为p2
e = proto.Unmarshal(b, p2)
```

# grpc

111



222

333

# 反射

aaaaaaaaaa

```go
// a是一个interface{}就行
// typ是reflect.Type类型
typ := reflect.TypeOf(a)

// 这个类型有几个方法？num就是方法的个数
num := typ.NumMethod()

// 取这个类型的第8个方法(从0开始)
method := typ.Method(8)


NumField()



// golang中必须指定这个玩意儿！真他妈的蠢！
option go_package = "./;hahaha";

// package在golang中有TMD什么用？
package test;

enum PhoneType {
    HOME = 0;
    WORK = 1;
}

message Phone {
    PhoneType type = 1;
    string number = 2;
}

message Person {
    int32 id = 1;
    string name = 2;
    repeated Phone phones = 3;
}



NumMethod()	// struct的method数量
Method(1)	// 获取第1个method，reflect.Method类型，再次获取.Type，可以获取到Type类型
NumField()	// 返回struct的字段数
Field(1)	// 返回第1个字段，reflect.StructField类型，再次获取.Type，可以获取到Type类型

// 对于func类型的Type
NumIn()  	// 返回参数的个数
NumOut()  	// 返回返回值的个数
In(1)   	// 返回第1个参数(从0开始)，Type类型
Out(0)  	// 返回第0个返回值(从0开始)，Type类型












```

# 时间

```go
// 2006-01-02 03:04:05 PM -07:00
// 2006-01-02 15:04:05 -07:00
time.Now().Format("2006-01-02 15:04:05 -07:00")
```







# 好玩的

## byte()强制转换

```go
// uint16 65280 二进制表示为 11111111 00000000
var a uint16 = 65280
b := byte(a)
// 请问b为11111111还是00000000
// 答案是b为00000000
print(b)
// 如果我想要a的11111111部分怎么办呢？
b = byte(a >> 8)

```

## slice切片

```go
// a的len=10, cap=10
a := make([]int, 10)
b := a[:0]
// b的len和cap是多少呢？
fmt.Println(len(b), cap(b))
// b的len=0, cap=10。而且b与a共用相同的底层数组
//向b中append5个数
b = append(b, 1, 2, 3, 4, 5)
fmt.Println(a, b)
// 可以发现，a，b都被添加了1,2,3,4,5，这是因为a,b的底层数组是同一个东西
```

## slice切片

```go
a := make([]int, 10, 20)
b := a[:15]
// 请问会报错么？a的len只有10，但是b却取15
// 答：不会报错，因为a的容量有20，如果取的超过20，才会报错
// 并且a,b依然共享同一个底层数组
```

## nil

```go

```

## slice作为函数参数

```go
package main

import "fmt"

func main() {
	a := []string{"0"}
    // abc想给a数组添加几个元素，想得美，门儿都没有
    // 与map形成强烈对比
	abc(a)
	fmt.Println(a)
}

func abc(l []string) {
	l = append(l, "1")
	l = append(l, "2")
	l = append(l, "3")
	l = append(l, "4")
	l = append(l, "5")
	l = append(l, "6", "7", "8", "9")
    // l已经重新分配内存了，所以这些新增的元素，反应不到外部的l
    // 如果l不重新分配内存，那么l的变化会反应到外部的l
}
```

## map作为函数参数

```go
package main

import "fmt"

func main() {
	a := map[string]string{"0": "0"}
    // abc函数可以改变a参数，即使使a变大也没事
    // abc函数运行完之后，a参数真的变变了
	abc(a)
	fmt.Println(a)
}

func abc(m map[string]string) {
	m["1"] = "1"
	m["2"] = "1"
	m["3"] = "1"
	m["4"] = "1"
	m["5"] = "1"
	m["6"] = "1"
	m["7"] = "1"
	m["8"] = "1"
	m["9"] = "1"
    // 可以随意给m添加值，添加任意多个都没事，即使底层重新分配内存也不碍事
}
```

为什么map会这样？golang的作者说了，用户创建的`map`其实是`*map`。在很早以前的golang，确实需要将`map`定义为`*map`，后来发现程序员只定义`*map`，从来不定义`map`，索性直接用`map`代替`*map`了。是的，就是这么随意！操！

# Redis

核心，连接redis(Dial)，操作redis(Do)

```go
package main

import (
	"fmt"

	"github.com/gomodule/redigo/redis"
)

func main() {
	// 先创建几个DialOption玩儿玩儿
	// DialOption用于配置redis客户端
	// 比如设置客户端名字(命令为CLIENT SETNAME haha)
	// 使用密码登陆redis(命令为AUTH your_password)
	// 使用用户+密码登陆redis(命令为AUTH your_name your_password)
	// 等等...
	ocn := redis.DialClientName("tanghttest")
	opw := redis.DialPassword("Tht940415,./")
	// Dial接收N个DialOption选项,上面创建的，这里给它传递进去就行了
	c, e := redis.Dial("tcp", "www.tanght.xyz:6379", ocn, opw)
	if e != nil {
		fmt.Println("连接redis失败", e.Error())
	}
	// 然后就可以使用c了，c是redis的连接，通过c给redis发命令就行了
	// redis返回的是interface类型，可以使用redis包提供的类型转换函数进行转换
	// 比如redis.String()将redis的返回值转换为string类型
	fmt.Println(redis.String(c.Do("GET", "tanght")))
	fmt.Println(redis.String(c.Do("SET", "tanght", "100")))
	fmt.Println(redis.String(c.Do("GET", "tanght")))
}
```

连接池

```go
package main

import (
	"fmt"
	"time"

	"github.com/gomodule/redigo/redis"
)

func main() {
	p := redis.Pool{MaxIdle: 10, MaxActive: 100, Dial: redisDial, IdleTimeout: 10 * time.Second}
	c := p.Get()
	defer c.Close()
	fmt.Println(redis.String(c.Do("GET", "tanght")))
	fmt.Println(redis.String(c.Do("SET", "tanght", "100")))
	fmt.Println(redis.String(c.Do("GET", "tanght")))
	fmt.Println("haha")
}

func redisDial() (redis.Conn, error) {
	ocn := redis.DialClientName("haha")
	opw := redis.DialPassword("xxxx")
	return redis.Dial("tcp", "www.abc.com:6379", ocn, opw)
}
```

# 标准库

## bytes

提供字符串处理常用方法，比如字符串分割，字符串比较，搜索子字符串，字符串数组join，字符串替换等等。

提供一个buffer，可以从里面读数据(Reader)或向里面写数据(Writer)。

提供一个Reader，跟buffer有什么不同？我也不知道，感觉跟buffer类似了。

### 常用函数

```go
// 按照sep为分隔符切割s，将s分割为一堆小s，分隔符直接扔掉，小s中不带分隔符
func Split(s, sep []byte) [][]byte

// 与Split功能一样，只不过分割后的小s中带有sep，也就是说每个小s都带一个sep尾巴(最后一个小s可能没有分隔符)
func SplitAfter(s, sep []byte) [][]byte

// 与Split一样，只不过[][]byte的长度最大为n
func SplitN(s, sep []byte, n int) [][]byte

// 还有一堆常用的，自己看源码中的注释就行了
```

### bytes.Buffer

NewBuffer()创建一个Buffer，然后就可以对这个Buffer进行读写了。

记住，写入的话是从内部buf的len()处开始写的，所以如果想从头开始写，那一定要创建一个len为0(cap可0可不0)的[]byte给NewBuffer进行初始化。

![image-20211228153826039](assets/image-20211228153826039.png)

![image-20211228153753199](assets/image-20211228153753199.png)

## bufio

123

![image-20211228164332935](assets/image-20211228164332935.png)

## json

结构体Tag的规则：

- 结构体字段后面用反引号包裹起来的字符串就是Tag
- 字符串是一堆key-value对，用空格将各个key-value对分割开
- key不能用双引号包裹，value必须用双引号包裹(因为value中可能包含空格)
- 可以用反射功能在代码中获取结构体各字段的Tag
- Tag的作用就是给结构体的字段增加一个辅助字符串

```go
package main

import (
	"fmt"
	"reflect"
)

type ABC struct {
	A int `dog:"我是一只狗" 猫:"i am cat"`
	B int
}

func main() {
	abc := ABC{}
	tag1 := reflect.TypeOf(abc).Field(0).Tag.Get("dog")
	fmt.Println(tag1)  // 我是一只狗
	tag2 := reflect.TypeOf(abc).Field(0).Tag.Get("猫")
	fmt.Println(tag2)  // i am cat
}
```

既然Tag能给结构体的字段附带一些信息，那么json库就利用了Tag来定义了一些规则，来辅助json编解码

```golang
// json库只获取Tag的名字为"json"的Key
// 对于下面的ABC.A字段,json库只会取到"A,string"这个字符串
// "required,min=6,max=20"这个value是不会被获取到的
type ABC struct {
	A int `json:"A,string" validate:"required,min=6,max=20"`
	B string
}

// A,string：A是定义json字段的名字，因为json字段的名字可能跟结构体中字段的名字不一致
// A,string：string是定义json字段的类型
// 在golang中ABC.A的类型为int，在json中A的类型为string
// {"A": "1"}  {"A": 1} 的区别
type ABC struct {
	A int `json:"A,string" validate:"required,min=6,max=20"`
}
```

编解码

```go
// 将字符串str按照abc结构体的格式，转换成abc结构体
json.Unmarshal(str, &abc)

// 将abc结构体变成json字符串
json.Marshal(abc)
```

## atomic

```go
// CAS(CompareAndSwap)操作的意思: 如果 A==B 则将A设置为C并返回true
// 如果*addr == old 则 *addr=new
// 因为要修改addr的值, 所以要将addr的指针传进去
atomic.CompareAndSwapPointer(addr *unsafe.Pointer, old unsafe.Pointer, new unsafe.Pointer) (swapped bool)
```







## net

- 多个协程同时对1个`net.Conn`执行`Write`操作是安全的
- 多个协程同时对1个`net.Conn`执行`Read`操作是无意义的，所以我没测试
- 数据顺序不会出错，比方说2个协程，一个写"1111"另一个写"2222"，那么对方不会收到类似"11221122"这种信息
- 猜测Write内部是有并发考虑的，可能是内部加锁了
- 多个协程同时对1个`net.Conn`写，不如1个协程的效率高，所以最好借助`chan`

```go
func main() {
	l, _ := net.Listen("tcp", "127.0.0.1:8000")
	c, _ := l.Accept()
	for i := 0; i < 100; i++ {
		go write(c)
	}
	time.Sleep(10000 * time.Second)
}

func write(c net.Conn) {
	for {
		c.Write([]byte("123"))
	}
}
```

