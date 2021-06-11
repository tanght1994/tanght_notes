# 命令

## 生成私钥

```shell
openssl genrsa -out private.key 1024
```

- -out指定输出文件的名字

## 生成证书请求文件

```shell
openssl req -new -out server.csr -key private.key
```

- -out指定输出文件的名字
- -key指定自己的私钥（已经提前生成了）

## 生成公钥

```shell
openssl rsa -in private.key -pubout -out public.key
```

- -in指定输入文件的名字
- -pubout告诉openssl我要根据私钥生成公钥
- -out指定输出文件的名字

## 自签发（生成证书）

```shell
openssl ca -selfsign -in ca.csr
```

- -in指定请求文件，生成这个请求文件的证书

## 给别人签发

```shell
openssl ca -in other.csr
```

# 配置文件

位置etc/ssl/openssl.cnf

## CA_default

CA_default段配置了ca子命令相关配置，比如说签发完的证书存放的位置，ca证书的位置，ca私钥的位置等等



