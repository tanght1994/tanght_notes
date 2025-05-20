import os

# 递归获取 path 目录下所有的 md 文件的绝对路径
def get_all_md_files_path(path):
    if not os.path.isdir(path):
        return []
    all_files = []
    for root, _, files in os.walk(path):
        absroot = os.path.abspath(root)
        for file in files:
            if file.endswith('.md'):
                all_files.append(os.path.join(absroot, file))
    return all_files

# 获取当前目录以及子目录下所有的md文件内容
def get_all_md_files_content(path):
    all_files = get_all_md_files_path(path)
    all_content = ''
    for file in all_files:
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()
            all_content += content
    return all_content

# 获取 path 目录下所有文件的名字
def get_all_files_name(path):
    if not os.path.isdir(path):
        return []
    for _, _, files in os.walk(path):
        return files
    return []

# 获取 assets 文件夹中所有图片的名字
def get_all_picture_name(path):
    return get_all_files_name('assets')

# 获取没有的图片名字
def get_unused_picture_name():
    abspath = os.path.abspath('./assets')
    all_picture_name = get_all_picture_name(abspath)
    all_md_content = get_all_md_files_content('.')
    unused_picture_name = []
    for picture_name in all_picture_name:
        if picture_name not in all_md_content:
            unused_picture_name.append(os.path.join(abspath, picture_name))
    return unused_picture_name

# 删除没用的图片
def remove_unused_picture():
    unused = get_unused_picture_name()
    print('以下图片将要被删除：')
    for picture in unused:
        print(picture)
    confirm = input('是否删除这些图片？(y/n): ')
    if confirm.lower() == 'y':
        for picture in unused:
            os.remove(picture)
        print('删除成功')
    else:
        print('取消删除')

if __name__ == '__main__':
    remove_unused_picture()