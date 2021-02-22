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

