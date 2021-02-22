MySQL语句

```mysql
show full processlist;						# 查看当前进程列表
show variables like '%max_connections%';	# 查看最大连接数
show variables like 'xxxxx';				# 查询mysql的系统变量
set xxx = “123”;							# 设置mysql系统变量的值
show variables like 'event_scheduler';		# 查询event是否开启
SHOW EVENTS;								# 查询系统中所有event

# 字符集
show variables like '%char%';				#查看字符集
character_set_client
character_set_connection
character_set_database
character_set_filesystem
character_set_results
character_set_server
character_set_system
character_sets_dir


# 插入数据
INSERT INTO table_name (id, name,age) VALUES (1, "xiaoming", 18);

# 查询第0条数据以及往后1000条
SELECT * FROM xxxname LIMIT 0, 1000;

# 删除一段时间的数据
# ct为mysql的时间格式，直接跟字符串比较就行了
DELETE FROM xxxname WHERE ct > '2020-01-06 00:00:00' and ct < '2020-01-07 00:00:00';

# 查询test数据库所占用的空间
# 原理：MySQL软件中存在一个information_schema数据库，这个数据库保存了其它所有数据库的基本信息。
# 原理：information_schema数据库中存在一张表，名字为TABLES，这张表中有我们需要的数据（占用空间）
SELECT SUM(DATA_LENGTH) FROM TABLES WHERE TABLE_SCHEMA='test';	# 单位为字节


# 如果test1表存在，则将他删除
DROP TABLE IF EXISTS test1;	

# 创建表（test1不存在时才创建，若已经存在，则什么都不做）
CREATE TABLE IF NOT EXISTS test1 (
  id INT NOT NULL AUTO_INCREMENT,	# NOT NULL说明不能为空，AUTO_INCREMENT自增
  nick_name VARCHAR(255) NOT NULL,
  uid VARCHAR(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
	age INT NOT NULL DEFAULT 0,
  gmt_create datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  gmt_modified datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;


# 创建用户
CREATE USER 'haha1'@'%' IDENTIFIED BY '123456';	#  %表示可以从任何主机登陆
CREATE USER 'haha2'@'192.168。20.%' IDENTIFIED BY '123456';	# 20网段的可以登录

# 删除用户
DROP USER 'username'@'host';

# 修改密码
SET PASSWORD FOR 'root'@'localhost' = PASSWORD('123456');

# 授权
GRANT 权限 ON 数据库.表名 TO '账户名'@'主机';
GRANT SELECT, INSERT ON test.user TO 'tht'@'%';#tht可以访问test数据库下的user表格，拥有S、I权限
GRANT ALL ON test.* TO 'tht'@'%';#tht可以访问test数据库下的所有表，对所有表拥有满权限

# 撤销授权
REVOKE 权限 ON 数据库.表名 FROM '账户名'@'主机';

# 修改数据
UPDATE <表名> SET 字段 1=值 1 [,字段 2=值 2… ] [WHERE 子句 ];

# /etc/mysql/debian.cnf配置文件记录了debian-sys-maint超级用户的密码，可以通过这个用户来修改其它人的密码，包括root用户
# 必须用sudo打开这个文件，否则看不到文件内容
# /etc/mysql/mysql.conf.d/mysqld.cnf中bind-address = 127.0.0.1这一行要注释掉，否则这个mysql只能在本地用，外界不能访问


use mysql;
update mysql.user set authentication_string=password('root') where user='root' and Host ='localhost';
update user set plugin="mysql_native_password"; 
flush privileges;
quit;
sudo service mysql restart
mysql -u root -p 

```



储存过程

```mysql
SET @abc = 10;	# 声明+设置局部变量
SET bcd = 20;	# 设置系统变量，必须得是系统中有的变量才能设置

# 储存过程中给变量设置值 SELECT INTO
SET @mark_time = '2020-01-01 00:00:00';
SELECT DATE_SUB(CURRENT_TIMESTAMP(),INTERVAL 93 DAY) INTO @mark_time;

# 有些语句不能在储存过程中使用，可以使用预备语句
SET @mark_id = 0;
SET @sql_get_mark_id = CONCAT('SELECT id INTO @mark_id FROM ', param_table_name, ' WHERE gmt_create > "', @mark_time, '" LIMIT 1;');
PREPARE stmt FROM @sql_get_mark_id;
EXECUTE stmt;
```



创建表相关：

```mysql
USE `test`;	#在test数据库中创建表	`这个符号是mysql的转义符号
CREATE TABLE test01 (
  `id1` bigint unsigned NOT NULL AUTO_INCREMENT COMMENT 'xxxxx',
  `id2` int NOT NULL DEFAULT 0
  `id3` int NOT NULL DEFAULT 0
  `id4` int NOT NULL DEFAULT 0
  `id5` int(11) NOT NULL COMMENT 'xxxx',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '',
  `modified_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '最后修改时间',
  PRIMARY KEY (`id2`,`id3`),
  UNIQUE KEY `uniq_id` (`id1`) USING BTREE,
  INDEX `idx_id4` (`id4`) USING BTREE # 索引
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

# `这个符号是mysql的转义符号，如果创建的表名或字段名与mysql的关键字冲突了，则需要使用``包起来；
# USE `test` 表示在test数据库中创建表；
# COMMENT 'xxx' COMMENT关键字的意思是，后面的内容为注释；
# int(11) 创建一个int类型的字段，（11）没用，数据位数只跟类型有关，跟（）中的数字无关；
# AUTO_INCREMENT关键字是自增的意思，也就是说下一条数据是上一条数据+1，向表中插入数据的时候，不用填充被AUTO_INCREMENT修饰的字段；
# 被NOT NULL修饰的字段不允许为空，也就是说在插入数据的时候，NOT NULL字段必须有值；
# DEFAULT 默认值，带有默认值的字段，即便为NOT NULL，在插入的时候也可以不填充数据，因为如果没有值的话，他就会被默认值填充，所以依然不为空，满足NOT NULL的条件；
# id1被设置为自增的，所以它必须是唯一的(UNIQUE KEY);
```









错误 "this is incompatible with sql_mode=only_full_group_by"

```sql
-- 查看系统变量sql_mode，可以看到sql_mode中带有ONLY_FULL_GROUP_BY这个值，就是这个值造成了这个错误
show variables like "sql_mode"

-- 解决办法，使用sql语句（临时）重新设置这个系统变量，删除ONLY_FULL_GROUP_BY这个值，其它的保持不变
set @@GLOBAL.sql_mode=STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION
-- 解决办法，在mysql的配置文件（my.cnf）中设置这个系统变量，删除ONLY_FULL_GROUP_BY这个值，其它的保持不变，永远生效
sql_mode=STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION
```





函数

```sql
-- 字符串连接，若str1，str2，strN中有一个为NULL，返回值则为NULL
concat("str1","str2","str3",...)
-- 尽管id或score不是string类型，也当作string类型进行连接
select concat (id, name, score) as info from test1

-- 使用 连接符 进行字符串连接
concat_ws("连接符", str1, str2, ...)

-- 分组字符串连接
group_concat()
-- 使用名字分组，也就是说相同名字的记录只显示一条，这时候将相同名字的id连接到一起返回给我
select name, group_concat(id) from test group by name
-- 还可以指定连接的时候的排序和分隔符(排序order by id desc)(分隔符separator "+")
select name, group_concat(id order by id desc separator "+") from test group by name
```









