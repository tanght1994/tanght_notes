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

# 证书签发的过程

1.拥有根证书(A)

2.使用根证书(A)，签其它服务器的证书(B)

3.使用根证书(A)，签其它服务器的证书(C)

4.使用根证书(A)，签其它服务器的证书(D)

。。。。。。

5.将证书B配置到Nginx的证书上(同时将证书的密钥也配置上)

6.客户端信任根证书A(预制在操作系统中，或者用户手动将A导入到设备的可信任的证书中)

所以我要自己制作根证书A！

# 制作根证书

openssl超级垃圾！巨难用！

```shell
mkdir demoCA || exit
cd demoCA || exit
mkdir newcerts private temp || exit
touch serial index.txt || exit
echo 01 > serial || exit
cd private || exit
openssl rand -out .rand 1000 || exit
openssl genrsa -out cakey.pem 4096 || exit
cd ../temp
cat <<EOF > ca.conf
[ req ]
default_bits = 4096
req_extensions = req_ext
distinguished_name = req_distinguished_name

[ req_distinguished_name ]
countryName                 = countryName
countryName_default         = CN
stateOrProvinceName         = stateOrProvinceName
stateOrProvinceName_default = BeiJing
localityName                = localityName
localityName_default        = BeiJing
organizationName            = organizationName
organizationName_default    = THT
commonName                  = commonName
commonName_default          = TangHongTao
commonName_max              = 64

[ req_ext ]
basicConstraints = CA:true
keyUsage = critical, keyCertSign
EOF
cd ..
openssl req -new -key private/cakey.pem -out temp/ca.csr -config temp/ca.conf
openssl x509 -req -days 3650 -in temp/ca.csr -signkey private/cakey.pem -out private/cacert.pem
cd ..
echo success
```

至此，成功创建根证书，可以用根证书来给服务器签发证书了。

# 使用根证书签服务器证书

编写server.conf文件

```shell
[ req ]
default_bits       = 2048
distinguished_name = req_distinguished_name
req_extensions     = req_ext

[ req_distinguished_name ]
countryName                 = countryName
countryName_default         = CN
stateOrProvinceName         = stateOrProvinceName
stateOrProvinceName_default = BeiJing
localityName                = localityName
localityName_default        = BeiJing
organizationName            = organizationName
organizationName_default    = JJ
commonName                  = commonName
commonName_default          = www.tanght.xyz

[ req_ext ]
subjectAltName = @alt_names

[alt_names]
DNS.1 = www.tanght.xyz
DNS.2 = localhost
IP.1 = 127.0.0.1
```

然后执行以下3条命令生成服务器证书

```shell
# 生成私钥server.key
openssl genrsa -out server.key 2048
# 生成证书请求文件server.csr
openssl req -new -key server.key -out server.csr -config server.conf
# 使用根证书签发服务器证书
openssl x509 -req -days 3650 -CA ../demoCA/private/cacert.pem -CAkey ../demoCA/private/cakey.pem -CAcreateserial -in server.csr -out server.crt -extensions req_ext -extfile server.conf
```

