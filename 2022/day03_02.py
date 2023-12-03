from day03_01 import PRIORITIES, INPUT

def parse_elf_groups(fpath, group_size = 3):
    group_idx = 0
    contents = []
    with open(fpath, 'rt') as f:
        for row in f:
            contents.append(set(row.strip()))
            if group_idx == group_size - 1:
                shared_item = contents[0].intersection(*contents[1:])
                yield list(shared_item)[0]
                group_idx = 0
                contents = []
            else:
                group_idx += 1

if __name__ == '__main__':
    print(sum(PRIORITIES[i] for i in parse_elf_groups(INPUT)))
