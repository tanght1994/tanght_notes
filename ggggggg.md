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

