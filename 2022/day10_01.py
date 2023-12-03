from collections import deque, namedtuple
import math
import re
from typing import Iterable

Instruction = namedtuple('Instruction', ['instruction', 'amount', 'cycles'])

instruction_pattern = re.compile(r"^(?P<ins>(noop|addx))\s*(?P<amt>\-?[0-9]+)?$", re.I)

INSTRUCTION_CYCLES = {'noop': 1, 'addx': 2}

def parse_instruction(x):
    instruction_match = re.match(instruction_pattern, x)
    instruction = instruction_match['ins']
    amount = int(instruction_match['amt']) if instruction_match['amt'] is not None else None
    cycles = INSTRUCTION_CYCLES[instruction_match['ins']]

    return Instruction(instruction, amount, cycles)

def read_instructions_from_input(fpath):
    with open(fpath, 'rt') as f:
        for row in f:
            yield parse_instruction(row.strip())


def run_instructions(instructions: Iterable[Instruction], 
                     init_value: int = 1) -> deque:
    
    reg_values = [init_value]
    for ins in instructions:
        curr_value = reg_values[-1]
        
        for c in range(ins.cycles - 1):
            reg_values.append(curr_value)
        
        if ins.instruction == 'noop':
            reg_values.append(curr_value)
        elif ins.instruction == 'addx':
            reg_values.append(curr_value + ins.amount)
        else:
            raise ValueError(f"Uknown instruction {ins.instruction}.")

    return reg_values

def compute_cycle_values(register_values):
    return [(i + 1) * v for i, v in enumerate(register_values)]

def draw_pixel(cycle, reg_values, screen_width):
    row = (cycle - 1) // screen_width
    position = (cycle - 1) - (screen_width) * row

    if reg_values[cycle - 1] - 1 <= position <= reg_values[cycle - 1] + 1:
        pixel = '#'
    else: 
        pixel = '.'
        
    return pixel
    
def draw_screen(reg_values, crt_width, crt_height):
    cycle = 1
    screen = []
    for row in range(crt_height):
        for col in range(crt_width):
            screen.append(draw_pixel(cycle, reg_values, crt_width))
            cycle += 1
        screen.append('\n')
    return ''.join(screen)


INPUT = 'day10_input.txt'

if __name__ == '__main__':
    instructions = read_instructions_from_input(INPUT)
    reg_values = run_instructions(instructions)
    cycle_values = compute_cycle_values(reg_values)

    cycles = [20, 60, 100, 140, 180, 220]

    print(sum(cycle_values[i-1] for i in cycles)) # 17020

    crt_width = 40
    crt_height = 6
    
    screen = draw_screen(reg_values, crt_width, crt_height)

    print(screen)