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

## 字符串拼接

key：字符串拼接，字符串模板，字符串插值，字符串大括号

```javascript
const name = 'tanght'
const haha = `Hello ${name}!`
```

