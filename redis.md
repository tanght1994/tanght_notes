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