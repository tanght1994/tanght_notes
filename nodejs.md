# NPM

## 初始化项目

在一个空文件夹中执行`init`命令，执行完之后会生成`package.json`文件

```shell
npm init
```

## 安装三方包

必须先`init`初始化自己的项目才能`install`其它包

```shell
# 本地安装(安装包的所有文件都会保存在./node_modules/xxx文件夹下)
npm install package_name

# 全局安装(安装包的所有文件都会保存在/xxx/xxx/xxx/node_modules/xxx文件夹下)
npm install package_name -g

# 安装到dependencies
npm install xxx -S

# 安装到devDependencies
npm install xxx -D
```

## 运行别人的项目

下载了别人的项目后，首先要安装这个项目的所有依赖，这个项目所有的依赖都记录在了`package.json`文件中，我们只要通过一条命令就能自动安装所有包到`./node_modules`目录下

```shell
npm i
```

# JS

教程：https://zh.javascript.info/js

## 字符串拼接

key：字符串拼接，字符串模板，字符串插值，字符串大括号

```javascript
const name = 'tanght'
const haha = `Hello ${name}!`
```

## promise

```javascript
new Promise(function(resolve, reject) {
  setTimeout(() => resolve(1), 1000);
})

fetch('url1').then(res => {
    console.log(res)
    return fetch('url2')
})
.then(res => {
    console.log(res)
    return fetch('url3')
})
.then(res => {
    console.log(res)
})
```

## async & await

用async修饰的函数，返回值是Promise，即便代码中写的返回值不是Promise，编译器也将返回值包装为Promise

```javascript
async function haha() {
    return 1 // 即使1不是Promise，编译器也会将1修改为Promise
}

// return 1 被编译器修改为下面的代码
// async function haha() {
//     return new Promise((resolve, reject) => {
//         resolve(1)
//     })
// }

haha().then(x => console.log(x))
```

await用于阻塞代码，直到await处的代码执行完毕才继续向下执行

await之能用于被async修饰的函数中（因为不能给await阻塞主协程的机会）

```javascript
async function f() {

  let promise = new Promise((resolve, reject) => {
    setTimeout(() => resolve("done!"), 1000)
  });

  let result = await promise; // 等待，直到 promise resolve (*)

  alert(result); // "done!"
}

f();
```

## export & import

这两个关键字是ES6新语法，与`const xxx = require('xxx')`功能一样，都是导入导出的作用。

nodejs中使用ES6，文件后缀必须是.mjs

```javascript
// 想要导出哪个变量，就把export关键字添加上
export const a = 100
const b = 200
export const c = a + b

// 或者可以先定义变量，然后在最后一行统一export
const a = 100
const b = 200
const c = a + b
export { a, c }

// 如何引用别的文件中的内容呢？
// 加入./a文件中导出了haha和xixi和other变量
import {haha, xixi} from './a' // 从./a中引入haha和xixi两个变量，且只引入这两个
import * as abc from './a'     // 从./a中引入所有内容, 并用abc.haha调用
```
export default

当一个文件只向外导出1个东西时，可以使用export default

正常情况下，import外部内容时，要`import {xxx} from 'xxx'`，大括号中的名字必须是包内已导出的名字

export default之后，只需要`import haha from 'xxx'`，连大括号都不用了

```javascript
// 当一个文件只向外导出1个东西时，可以使用export default
const tanght = 10
export default

// 别人这样导入
import a from './a'
log(a)  // 这里的a就是tanght
```

## require & module.exports

```javascript
module.exports = 'abc'
```

