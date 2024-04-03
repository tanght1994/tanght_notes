# MySQL

# Redis

# MongoDB

mongodb无需创建数据库，也无需创建表，插入数据的时候如果数据库或表不存在，则自动创建。

如果一个表还未存在，你也可以提前对它创建索引，当这个表被创建出来的时候索引就生效了。

## 安装

https://www.mongodb.com/docs/manual/tutorial/install-mongodb-on-red-hat/

![image-20240122164339965](./assets/image-20240122164339965.png)



/etc/yum.repos.d/mongodb-org-7.0.repo

```
[mongodb-org-7.0]
name=MongoDB Repository
baseurl=https://repo.mongodb.org/yum/redhat/7/mongodb-org/7.0/x86_64/
gpgcheck=1
enabled=1
gpgkey=https://www.mongodb.org/static/pgp/server-7.0.asc
```



sudo yum install -y mongodb-org

sudo systemctl daemon-reload

sudo systemctl start mongod

mongosh

创建超级用户

```
use admin
db.createUser(
  {
    user: "root",
    pwd: "dtfh45h",
    roles:
    [ "root"]
  }
)
```

vim /etc/mongod.conf

```
127.7.7.1 -> 0.0.0.0
security:
  authorization: enabled
```

sudo systemctl stop mongod

sudo systemctl start mongod

mongosh  -u root -p dtfh45h



## 超级管理员

mongodb的用户时针对单个数据库的，比如数据库A中的用户与数据库B中的用户时完全隔离的。不存在可以操作所有数据库的用户。超级管理员可以操作所有数据库。

mongodb刚安装完成时，只允许从localhost访问，且不需要用户密码。这时可以创建超级管理员。

```shell
use admin
db.createUser( { user: 'root', pwd: '123456', roles: ['root'] })
```

roles为root的用户就是超级管理员。

创建完超级管理员之后就可以打开mongodb的远程访问了，并开启密码登录。

1. 创建超级管理员
2. 开启远程访问并开启密码登录

顺序一定不要错，如果你先开启密码登录，你就无法登录了！因为你还没创建超级管理员！

## partial index

部分索引的意思是，只有符合条件的数据才会被建立索引

比如将phone字段设置为唯一索引，那么整个表中只能存在1个没有phone字段的数据

```json
{"name": "tanght1", "age": 18, "phone": "13302166666"}
{"name": "tanght2", "age": 18}  X!唯一索引冲突
{"name": "tanght3", "age": 18}  X!唯一索引冲突
```

```json
{"name": "tanght1", "age": 18, "phone": "13302166666"}
{"name": "tanght2", "age": 18, "phone": ""}  X!唯一索引冲突
{"name": "tanght3", "age": 18, "phone": ""}  X!唯一索引冲突
```

只有存在phone字段且phone字段不是空字符串时才做唯一索引检查，需要使用部分索引

上述条件可以简化为phone字段大于""

```shell
db.xxx.createIndex({ phone: 1 }, { unique: true, partialFilterExpression: { phone: { $gt: "" } } })
```



## update修改

```shell
db.xxx.updateOne(
   { "d": "ddd" },
   { $set: { "a.b": "abab", "c": "ccc" }}
)
```

修改(aggregation)

```shell
db.xxx.updateOne(
   { "d": "ddd" },
   [
     { $set: { "a.b": "abab", "c": "ccc" }}
   ]
)


db.userinfo.updateOne({ userid: 10000001 },[{$set: {coin: {$add: ["$coin", 10]}}},{$set: {max_coin: {$max: ["$coin", "$max_coin"]}}}])
```



```shell
{$set: {abc: 100}}
{$set: {abc: {$min: [50, 100]}}}
{$set: {abc: {$min: [{$add: ["$abc", 10]}, 100]}}}
```



![image-20240111191640561](./assets/image-20240111191640561.png)

## mongosh

连接数据库

```shell
# 连接127.0.0.1:27017并使用test库
mongosh

# 连接127.0.0.1:27017并使用abc库
mongosh 127.0.0.1:27017/abc
```

使用密码

```shell
# -u指定用户 -p指定密码
mongosh 127.0.0.1:27017/abc -u root -p 123456
```

执行js语句

```shell
# 执行js语句后退出交互模式
mongosh 127.0.0.1:27017/tanght --eval "printjson(db.users.insertOne({ name: 'tanght', age: NumberLong(18) }))"
```

执行js脚本

```shell
# 执行js脚本后退出交互模式
mongosh 127.0.0.1:27017/abc abc.js
```

js脚本

```javascript
// NumberLong("10000001")指定字段类型
db.userinfo.createIndex({ userid: 1 }, { unique: true });
db.userinfo.createIndex({ fbid: 1 }, { unique: true, partialFilterExpression: { fbid: { $gt: "" } } });
db.userinfo.createIndex({ imei: 1 }, { unique: true, partialFilterExpression: { imei: { $gt: "" } } });
db.userinfo.createIndex({ createat: 1 });
db.userinfo.createIndex({ invite_code: 1 }, { unique: true });
db.userinfo.createIndex({ beinvited_code: 1 });

db.session.createIndex({ sessionid: 1 }, { unique: true });
db.session.createIndex({ userid: 1 }, { unique: true });
db.session.createIndex({ cts: 1 }, { expireAfterSeconds: 2592000 });

db.nextid.createIndex({ type: 1 }, { unique: true });
db.nextid.insertOne({ type: "userid", next: NumberLong("10000001") });
db.nextid.insertOne({ type: "invite_code", next: NumberLong("1") });
db.nextid.insertOne({ type: "roomid", next: NumberLong("1") });

db.domino_process.createIndex({ roomid: 1 }, { unique: true });
db.domino_process.createIndex({ userid: 1 });
db.domino_process.createIndex({ game_start: 1 });
```

