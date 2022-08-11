# 远程登录

whereis redis.conf

/etc/redis/redis.conf

修改redis.conf

将bind 127.0.0.1 ::1注释掉，替换成bind 0.0.0.0 ::1

protected-mode no改成protected-mode yes

# 设置密码

即使设置了密码，使用本机的redis-cli也不需使用密码

使用redis-cli登陆redis

config set requirepass返回值是空字符串，说明没有密码

config set requirepass 123456设置密码为123456

# 常见问题

## 缓存击穿

问题：大量的key同时过期，导致大量请求同时去mysql

解决方案：设置超时时间的时候，将超时时间随机10%

## 缓存穿透

问题：大量查询不存在的key，导致每次查询都需要去mysql

解决：即使查询不存在的key，也要将NULL缓存起来

