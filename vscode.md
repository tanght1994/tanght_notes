${workspaceFolder} :表示当前workspace文件夹路绝对路径。

${workspaceRootFolderName}:表示workspace的文件夹名，不是路径，仅仅是文件夹名而已。

${file}:文件自身的绝对路径。

${relativeFile}:文件相对路径，相对workspace来计算。

${fileBasenameNoExtension}:当前文件的文件名，不带路径，不带后缀（.json .cpp .txt等等都不要）。

${fileBasename}:当前文件的文件名，不带路径。

${fileDirname}:当前文件所在的文件夹绝对路径，不带文件名。

${fileExtname}:当前文件的后缀。

${lineNumber}:当前文件光标所在的行号。

${env:PATH}:系统中的环境变量。





```cmake
${VAR} # 取VAR变量的值
aux_source_directory(path, VAR) #将path目录下的所有源文件名字放到VAR变量中
file(GLOB _srcFiles "src/f[1-3].cpp") 
message("haha")
message(${VAR)


list(LENGTH var2 var3) # var2是一个数组，不用${var2}
```



# 配置文件系统介绍

打开配置文件，快捷键ctrl+,

![image-20210222183624657](assets/image-20210222183624657.png)

配置文件界面，本地与远程可以随意切换

![image-20210222184308951](assets/image-20210222184308951.png)

当前工作目录的setting.json可以覆盖全局的setting.json

也就是说将通用的配置写到全局的配置中，如果全局配置不适合当前项目，可以在当前项目中新建.vscode文件夹，在其中创建setting.json文件，用来局部覆盖全局配置



# C++配置文件

以下配置只影响C++程序的代码补全，并不影响gcc的编译

在全局的setting.json中放置通用的includePath，这样一来，那些普通的程序就可以补全了

```json
// 全局的setting.json文件
{
    "python.pythonPath": "venv/test/bin/python3.9",

    "C_Cpp.default.includePath": [
        "/usr/include/c++/7",
        "/usr/include/x86_64-linux-gnu/c++/7",
        "/usr/include/c++/7/backward",
        "/usr/lib/gcc/x86_64-linux-gnu/7/include",
        "/usr/local/include",
        "/usr/lib/gcc/x86_64-linux-gnu/7/include-fixed",
        "/usr/include/x86_64-linux-gnu",
        "/usr/include"
    ],
    "C_Cpp.default.intelliSenseMode": "linux-gcc-x64",
    "C_Cpp.default.cppStandard": "c++17",
    "C_Cpp.default.cStandard": "gnu11"
}
```

在当前项目的c_cpp_properties.json中设置特殊的配置

```json
// 当前项目的.vscode/c_cpp_properties.json文件
{
    "configurations": [
        {
            "name": "Linux",
            "includePath": [
                "${default}",
                "/home/tanght/download/boost_1_75_0"
            ],
            "defines": [],
            "compilerPath": "/usr/bin/gcc"
        }
    ],
    "version": 4
}
```

${default}是将全局setting.json的C_Cpp.default.includePath拿过来



# 无法在这个大型工作区监视

```json
//当前工作区的setting.json
{
    "files.watcherExclude": {
        "**/.git/objects/**": true,
        "**/.git/subtree-cache/**": true,
        "**/node_modules/*/**": true,
        "**/.hg/store/**": true,
        "/home/tanght/cpp/**": true,
        "/home/tanght/download/**": true,
        "/home/tanght/python/**": true,
        "/home/tanght/venv/**": true
    }
}
```

files.watcherExclude设置vscode的监视忽略。

也就是说vscode会不监视这些文件夹的变化情况，除非手动刷新。

里面的路径需要是绝对路径，不能是相对于工程目录的相对路径，但是可以使用**/这种来匹配。



```json
//当前工作区的setting.json
{
    "files.exclude": {
        "**/.git": true,
        "**/.svn": true,
        "**/.hg": true,
        "**/CVS": true,
        "**/.DS_Store": true,
        "cpp": true
    }
}
```

files.exclude更狠，vscode不仅不监控，连显示都不显示了，直接当作不存在。

里面的路径必须是相对于vscode工程的相对路径。