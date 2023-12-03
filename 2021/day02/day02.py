'''Advent of Code 2021: Day 02
'''

import re
from typing import Iterable, Tuple

Position = Tuple[int, int]
Movement = Tuple[int, int]


def parse_movement(s: str) -> Movement:
    '''Parse a string movement command into horizontal and vertical position changes.
    
    E.g. 'down 5' -> (0, 5); 'forward 3' -> (3, 0)
    '''
    directions = {'up': (0, -1), 'down': (0, 1), 'forward': (1, 0)}
    parsed = re.match(r'(?P<dir>^down|up|forward)\s+(?P<n>\d+)$', s)
    x, y = directions[parsed['dir']]
    n = int(parsed['n'])
    return (x * n, y * n)


def move(movements: Iterable[Movement], 
         initial_position: Position = (0, 0)) -> Position:
    '''Move the submarine.
    
    Returns the final position (horizontal, depth/vertical) after making all the movements.
    '''
    x0, y0 = initial_position
    return (x0 + sum(dx for dx, dy in movements), y0 + sum(dy for dx, dy in movements))


def move_by_aim(movements: Iterable[Movement], 
                initial_position: Position = (0, 0)) -> Position:
    '''Move the submarine using the aiming technique. Forward movement is scaled by the aim of the sub.
    
    Returns the final position (horizontal, depth/vertical) after making all the movements.
    '''
    aim = 0
    x, y = initial_position
    for (dx, dy) in movements:
        if dy != 0:
            aim += dy
        if dx != 0:
            x += dx
            y += aim * dx
    
    return (x, y)


def summarize_position(position):
    '''Summarize the position by multiplying the horizontal and vertical positions.
    '''
    x, y = position
    return x * y


# Example from the instructions
test_01 = '''forward 5
down 5
forward 8
up 3
down 8
forward 2'''


if __name__ == '__main__':
    input = 'day02_input.txt'

    # Test on instruction example
    assert summarize_position(move([parse_movement(m.strip()) for m in test_01.splitlines()])) == 150, "Test 1 failed"
    assert summarize_position(move_by_aim([parse_movement(m.strip()) for m in test_01.splitlines()])) == 900, "Test 2 failed"

    # Run on input
    with open(input, 'rt') as f:
        movements = [parse_movement(row.strip()) for row in f]
        print('Part 1:', summarize_position(move(movements)))
        print('Part 2:', summarize_position(move_by_aim(movements)))