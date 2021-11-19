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
# path：指定生成的xx.pb.go文件的位置
# package_name：指定xx.pb.go文件中，package的名字
# 下面是具体的例子，生成的文件在当前目录下，文件中的package名字是hahaha
option go_package = "./;hahaha";
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







# 好玩的

byte()强制转换

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

slice切片

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

slice切片

```go
a := make([]int, 10, 20)
b := a[:15]
// 请问会报错么？a的len只有10，但是b却取15
// 答：不会报错，因为a的容量有20，如果取的超过20，才会报错
// 并且a,b依然共享同一个底层数组
```

nil

```go

```







