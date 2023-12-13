from dataclasses import dataclass
from typing import Union, Iterator

@dataclass
class File:
    name: str
    size: int

@dataclass
class Directory:
    path: str
    childs: dict[str, Union[File, 'Directory']]
    parent: Union[None, 'Directory'] = None
    size: int = -1

def update_size(dir: Directory) -> int:
    dir_size = 0
    for child in dir.childs.values():
        match child:
            case File(_, size):
                dir_size += size
            case Directory():
                dir_size += update_size(child)
    dir.size = dir_size

    return dir_size

def parse_fs(raw: str)->Directory:
    root = Directory('/', {})
    pwd: Directory = root

    commands = [item.strip() for item in raw.split('$ ') if item.strip()]

    for command in commands:
        lines = command.split('\n')

        match lines:
            case ['ls', *results]:
                for line in results:
                    match line.split():
                        case ["dir", dirname]:
                            if dirname not in pwd.childs:
                                pwd.childs[dirname] = Directory(dirname, {}, parent=pwd)
                        case [size, filename]:
                            pwd.childs[filename] = File(name=filename, size=int(size))
            case [cd]:
                match cd.split():
                    case ['cd', '/']:
                        pwd = root
                    case ['cd', '..']:
                        pwd = pwd.parent if pwd.parent else pwd
                    case ['cd', dirname]:
                        if dirname in pwd.childs and isinstance(pwd.childs[dirname], Directory):
                            pwd = pwd.childs[dirname]
                        else:
                            raise ValueError('Unknown Directory %s', dirname)
    update_size(root)

    return root

def yield_dir_at_most(root: Directory, max_size: int=100_000) -> Iterator:
    if root.size <= max_size:
        yield root
    
    for child in root.childs.values():
        if isinstance(child, Directory):
            yield from yield_dir_at_most(child, max_size)

def total_size_at_most(root: Directory, max_size: int=100_000) -> int:
    return sum([item.size for item in yield_dir_at_most(root, max_size)])

RAW="""$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k"""

FS = parse_fs(RAW)
assert total_size_at_most(FS) == 95437

with open('day07.txt') as f:
    raw = f.read()

fs = parse_fs(raw)
print(total_size_at_most(fs))

total_disk_space = 70_000_000
needed_free_space = 30_000_000


def yield_dir_to_delete(root: Directory, min_size: int) -> Iterator:
    if root.size >= min_size:
        yield root
    
    for child in root.childs.values():
        if isinstance(child, Directory):
            yield from yield_dir_to_delete(child, min_size)

def find_smallest_dir_to_delete(root: Directory, total_disk_space: int=70_000_000, needed_free_space: int=30_000_000) -> int:
    min_size = needed_free_space - total_disk_space + root.size
    dir_list = list(yield_dir_to_delete(root, min_size))
    return sorted(dir_list, key=lambda item: item.size)[0].size

assert find_smallest_dir_to_delete(FS) == 24933642
print(find_smallest_dir_to_delete(fs))