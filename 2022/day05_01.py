from collections import deque
import re

def find_number_of_stacks_from_input(fpath: str) -> int:
    with open(fpath, 'rt') as f:
        for row in f:
            stack_labels = parse_stack_label_row(row)
            if len(stack_labels) > 0:
                return max(stack_labels)
        else:
            raise ValueError(f"Could not find stack label row in input {fpath}")
                
def read_stacks_from_input(fpath):
    stacks = []
    with open(fpath, 'rt') as f:
        for row in f:
            if len(parse_stack_label_row(row)) > 0:
                break
            else:
                parsed_stacks = parse_stack_input_row(row)
                stacks.append(parsed_stacks)
    return stacks

def parse_stack_input_row(row):
    parsed_row = []
    while len(row) >= 3:
        parsed_row.append(row[:4])
        row = row[4:]
    return [re.sub('[^A-Z]', '', x) for x in parsed_row]

def parse_stack_label_row(row):
    try:
        return [int(x) for x in re.split('\s+', row.strip())]
    except ValueError:
        return []

def create_stacks_from_list(lst):
    stacks = []
    for row in lst:
        for stack_no, item in enumerate(row):
            try: 
                stacks[stack_no]
            except IndexError:
                stacks.append(deque())
            if item != '':
                stacks[stack_no].append(item)
    return stacks

def move_stack_items(stacks, source: int, dest: int, n_times: int) -> None:
    for _ in range(n_times):
        item = stacks[source - 1].popleft()
        stacks[dest - 1].appendleft(item)
    return None

def move_stack_items_multi(stacks, source: int, dest: int, n_times: int) -> None:
    items = reversed([stacks[source - 1].popleft() for _ in range(n_times)])
    stacks[dest - 1].extendleft(items)
    return None

def read_instructions_from_input(fpath):
    instructions = []
    with open(fpath, 'rt') as f:
        for row in f:
            if is_instruction(row):
                instructions.append(parse_instruction(row))
    return instructions

INSTRUCTION_PATTERN = re.compile(r'^move (\d+) from (\d+) to (\d+)$', flags = re.I)

def is_instruction(txt):
    return re.match(INSTRUCTION_PATTERN, txt) is not None

def parse_instruction(txt):
    n_times, source, dest = re.match(INSTRUCTION_PATTERN, txt).groups(1)

    return {'source': int(source), 'dest': int(dest), 'n_times': int(n_times)}

def run_stack_movement_instructions(stacks, instructions, multi = False):
    for instruction in instructions:
        if multi:
            move_stack_items_multi(stacks, **instruction)
        else:
            move_stack_items(stacks, **instruction)
    return None


INPUT = 'day05_input.txt'


if __name__ == '__main__':
    stacks_01 = create_stacks_from_list(read_stacks_from_input(INPUT))
    stacks_02 = create_stacks_from_list(read_stacks_from_input(INPUT))

    instructions = read_instructions_from_input(INPUT)
    run_stack_movement_instructions(stacks_01, instructions)
    print("Part 1:", ''.join([stack[0] for stack in stacks_01]))

    run_stack_movement_instructions(stacks_02, instructions, multi = True)
    print("Part 2:", ''.join([stack[0] for stack in stacks_02]))