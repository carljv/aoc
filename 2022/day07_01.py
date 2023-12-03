from collections import deque, namedtuple
import re

Directory = namedtuple('Directory', ['path', 'children', 'files'])
File = namedtuple('File', ['name', 'size'])

chdir_pattern = re.compile(r'^\$ cd (?P<dirname>.+)$', flags = re.I)
ls_pattern =  re.compile(r'^\$ ls$', flags = re.I)
dir_pattern =  re.compile(r'^dir\s+(?P<dirname>.+)$', flags = re.I)
file_pattern = re.compile(r'^(?P<size>\d+)\s+(?P<filename>.+)$', flags = re.I)

def is_chdir(cmd):
    return re.match(chdir_pattern, cmd) is not None

def is_file(cmd):
    return re.match(file_pattern, cmd) is not None

def is_dir(cmd):
    return re.match(dir_pattern, cmd) is not None

def is_ls(cmd):
    return re.match(ls_pattern, cmd) is not None

def path_join(dirs):
    return re.sub('/+', '/', '/'.join(dirs))

def dir_size(dirname, file_tree):
    dir = file_tree[dirname]
    file_sizes = sum(f.size for f in dir.files)
    if len(dir.children) == 0:
        return file_sizes
    else:
        return file_sizes + sum([dir_size(path_join([dir.path, d]), file_tree) for d in dir.children])


def parse_commands(cmds):
    dir_hist = deque()
    filetree = {}
    is_listing = False

    for cmd in cmds:
        if is_chdir(cmd):
            is_listing = False
            dirname = re.match(chdir_pattern, cmd)['dirname']
            if dirname == '.':
                continue
            if dirname == '..':
                dir_hist.pop()
            else:
                dir_hist.append(dirname)
        if is_ls(cmd):
            path = path_join(dir_hist)
            is_listing = True
            filetree[path] = Directory(path = path, children = [], files = [])
            continue
        if is_listing and is_dir(cmd):
            dirname = re.match(dir_pattern, cmd)['dirname']
            filetree[path].children.append(dirname)
        if is_listing and is_file(cmd):
            file_match = re.match(file_pattern, cmd)
            _file = File(file_match['filename'], int(file_match['size']))
            filetree[path].files.append(_file)
    
    return filetree

def read_commands_from_input(fpath):
    with open(fpath, 'rt') as f:
        return [r.strip() for r in f.readlines()]


INPUT = 'day07_input.txt'


if __name__ == '__main__': 
    cmds = read_commands_from_input(INPUT)
    ftree = parse_commands(cmds)
    # dir_size('pqm', ftree) # 147513
    # dir_size('gtsf', ftree) # 1186199
    max_size = 100_000

    small_dirs = {d: dir_size(d, ftree) for d in ftree if dir_size(d, ftree) <= max_size}
    print("Small directories total:", sum(v for k, v in small_dirs.items())) # 1989474

    total_space = 70_000_000
    update_space = 30_000_000
    used_space = dir_size('/', ftree)
    available_space = total_space - used_space
    needed_space = max(0, update_space - available_space)
    print(f"Total space: {total_space}\nUsed space: {used_space}\nAvailable space: {available_space}\nNeeded space: {needed_space}")

    big_enough_dirs = {d: dir_size(d, ftree) for d in ftree if dir_size(d, ftree) >= needed_space}
    print("Smallest directory size:", min(v for k, v in big_enough_dirs.items())) # 1111607