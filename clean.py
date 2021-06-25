import re
import os


def get_picture_name_from_line(line):
    pattern = '!\[.*\]\((?P<picture_name>.*)\)'
    result = re.search(pattern, line)
    if result is None:
        return None
    return result.group('picture_name')


def get_picture_name_from_file(filename):
    result = []
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        for line in lines:
            picture_name = get_picture_name_from_line(line)
            if picture_name:
                result.append(picture_name)
    except Exception:
        pass
    finally:
        return result


def get_picture_name_from_dir(dirname):
    allnames = []
    for path, _, files in os.walk(dirname):
        allnames += [os.path.join(path, i) for i in files]
    mdnames = [i for i in allnames if len(i) > 2 and i[-3:] == '.md']
    all_picture_name = []
    for filename in mdnames:
        all_picture_name += get_picture_name_from_file(filename)
    return all_picture_name


def get_invalid_names():
    valid_names = get_picture_name_from_dir('.')
    all_names = []
    for path, _, files in os.walk('assets'):
        all_names = [os.path.join(path, i) for i in files]
        break
    valid_names = [i.replace('\\', '/').replace('//', '/') for i in valid_names]
    all_names = [i.replace('\\', '/').replace('//', '/') for i in all_names]
    invalid_names = set(all_names) - set(valid_names)
    return list(invalid_names)


def clean_picture():
    names = get_invalid_names()
    success = 0
    for i in names:
        try:
            os.remove(i)
            success += 1
        except Exception:
            pass
    return len(names), success


if __name__ == '__main__':
    try:
        needremove, remove = clean_picture()
        print(f'need remove count is {needremove}')
        print(f'success remove count is {needremove}', end='')
    except Exception:
        print('error')