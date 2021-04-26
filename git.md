# git登陆

```shell
以https克隆时，每次push都要输入密码，可以让git记住密码：
git config --global credential.helper store (开启记住密码功能，输入一次密码之后git会记下来)
```

![image-20200227111408413](assets/image-20200227111408413.png)

# git克隆

```shell
git remote add origin https://github.com/***/***.git
# 给 <https://github.com/***/***.git> 这个远程仓库取个别名叫做origin

git clone 远程仓库地址	#默认克隆master分支
git clone
git branch				#查看本地的所有分支
git branch -a			#查看所有分支（远程+本地）
git branch haha	   		#创建名字为haha的本地分支
git checkout haha		#切换到haha分支
git push --set-upstream origin test	//将当前分支与远程origin主机上的test分支建立联系
git push #将当前分支推送到远端相联系的分支
git pull <远程主机> <远程分支> <本地分支> #拉取远程分支到本地分支
git clone -b 分支名 远程仓库地址 # 克隆指定分支
```





# git fetch

使用`git branch -a`可以列出本地与远程的所有分支名字。但是如果远程仓库新增了一个分支，你电脑上的git是怎么知道远程仓库新增了一个分支呢？`git branch -a`可不负责联网去同步一下，那么谁负责呢？`git fetch`负责。

```shell
# 首先同步一下远程仓库
git fetch origin
# 然后再列出所有分支
git branch -a
```



```shell
git fetch origin 远程分支名:新建本地分支名
```





# git diff

```shell
# 比较当前工作目录与commitid的差别，只列出文件名字
git diff commitid --stat
```

- `git diff commitid --stat`：大苏打似的
- `git diff commitid --stat`：大苏打似的
- `git diff commitid --stat`：大苏打似的
- `git diff commitid --stat`：大苏打似的





# 放弃已经add后的文件的修改

- 先将这个文件由绿色变为红色（文件离开暂存区）
- 再对这个红色的文件checkout（对工作区中的变化进行还原）
- 因为绿色的文件无法checkout

```bash
git reset -q HEAD -- E:\test\2.txt    # 由绿色变为红色，仅仅是变色，文件内容并不会发生变化
git checkout -q -- E:\test\2.txt      # 再对红色的文件checkout，本次的所有修改都被还原

```



# 放弃没有add的文件的修改

```bash
git checkout -q -- E:\test\2.txt
```



# git status文件夹展开

```shell
git status -u
```



# 修改commit信息

```bash
git rebase -i HEAD~5
将准备修改的commit前改为r
```



# 合并多次commit

```bash
git rebase -i HEAD~5
前缀改为s
```



# 第一次推送至github(远程空仓库)

```bash
git init    			# 初始化本地仓库
git add *   			# 添加一些文件到暂存区
git commit -m "init"  	# 提交一次
git branch -M main		# 修改当前分支名为main
git remote add origin https://github.com/tanght1994/fishwebsdk.git # 添加远程仓库地址
git push -u origin main	# 推送到远程仓库
```



# 查看远程仓库信息

```shell
git remote show			# 列出所有远程仓库的别名
git remote show origin  # 查看origin详细信息
```

# 添加/删除远程仓库

```shell
git remote add origin https://github.com/tanght1994/fishwebsdk.git # 添加远程仓库地址,起别名为origin
git remote remove origin	# 删除别名为origin的远程仓库
```

# 分支

```shell
git branch -M main		# 修改当前分支的名字为main
git branch -D main  	# 删除main分支
git push origin --delete your_branch  # 删除远程分支
```



# .gitignore文件

子目录中也可以放置.gitignore文件，这时就不用写一层层的目录了，子目录中的.gitignore文件只关心自己当前目录的忽略就可以了

```shell
# .gitignore文件

*  				# 忽略所有文件/文件夹
!.gitignore  	# 除了.gitignore文件
!fishwebsdk/	# 除了fishwebsdk文件夹
!fishwebsdk/**	# 除了fishwebsdk下的所有文件和所有文件夹，并且是递归

# 顺序很重要，后面的代码会覆盖前面的代码
# 第一行代码  *  忽略了所有文件
# 但是后面的代码又将某些文件/文件夹排除了，所以那些文件/文件夹就不会被忽略了

/test.test # 忽略当前目录(本.gitignore文件所在的目录)下的test.test(文件或者目录都可以),其它目录或子目录并不会忽略test.test
test.test  # 忽略所有目录下的test.test
```





# GIT配置文件

## 查看

共有三个级别的配置文件，分别为，系统级，全局级，仓库级，优先级递增，后面的覆盖前面的

```shell
git config --system --list  # 只查看系统级配置
git config --global --list  # 只查看全局级配置
git config --local --list  # 只查看仓库级配置

# 查看所有配置项，系统级，全局级，仓库级，显示顺序是 系统级 全局级 仓库级
# 同一个配置项可以出现多次(比如在这三个级别中都设置了一次)，但是以最后出现的为准
git config --list

# 查看配置项,查看user.name
git config [--level] –-get user.name
```

仓库级配置文件(local)位置在.git/config，它的优先级是最高的

## 添加/修改

```shell
# 修改user.name为tanght1994，没有则添加
git config [--level] user.name tanght1994
```

## 删除

```shell
# 删除user.name
git config [--level] –-unset user.name
```

# 记住密码

```shell
git config --global credential.helper store
```