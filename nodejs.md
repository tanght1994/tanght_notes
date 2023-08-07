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

```javascript
```

