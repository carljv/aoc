from collections import Counter
from itertools import zip_longest
from math import abs
import re
from typing import Generator, Iterable, List, Tuple

Point = Tuple[int, int]
Line = Tuple[Point, Point]


def parse_line_spec(line_spec: str) -> Tuple[Point]:
    '''Create a line (pair of points) from a string.
    '''
    match = re.match('^(\d+)\,(\d+) \-> (\d+),(\d+)', line_spec)
    
    try:
        x0, y0, x1, y1 = (int(i) for i in match.groups())
    except (AttributeError, ValueError):
         raise ValueError(f'Could not parse line from "{line_spec}".')

    return ((x0, y0), (x1, y1))
    

def is_valid_line(line: Line, diagonal_allowed = True) -> bool:
    '''Check if a line is valid. 
    
    Valid lines are vertical, horizontal, or, if diagonal_allowed is True, 45º.
    '''
    x0, y0 = line[0]
    x1, y1 = line[1]
    dx = x1 - x0
    dy = y1 - y0

    not_sloped = x0 == x1 or y0 == y1
    is_45_degrees = abs(dy) == abs(dx) 

    if diagonal_allowed:
        return not_sloped or is_45_degrees
    else:
        return not_sloped
    

def points_on_line(line: Line, diagonal_allowed = True) -> List[Point]:
    '''Given a line (start and end point), list all the points the line goes through.
    '''
    
    assert is_valid_line(line, diagonal_allowed = diagonal_allowed), f"{line} is not a valid line."
    
    x0, y0 = line[0]
    x1, y1 = line[1]

    dx = 1 if x1 >= x0 else -1
    dy = 1 if y1 >= y0 else -1

    xs = list(range(x0, x1 + dx, dx))
    ys = list(range(y0, y1 + dy, dy))

    fill = x1 if len(ys) >= len(xs) else y1
        
    return list(zip_longest(xs, ys, fillvalue = fill))


def find_covered_points(lines: Iterable[Line], diagonal_allowed = True) -> Generator:
    '''For a set of lines, produce all the points covered by each line.
    
    Diagonal lines can be excluded.'''
    for line in lines:
        if is_valid_line(line, diagonal_allowed = diagonal_allowed):
            for point in points_on_line(line, diagonal_allowed = diagonal_allowed):
               yield point


def find_intersections(lines: Iterable[Line], diagonal_allowed: bool = True) -> List[Point]:
    '''Find all the points where at least two lines intersect. 
    
    Diagonal lines can be excluded.'''
    coverage = Counter(find_covered_points(lines, diagonal_allowed = diagonal_allowed))
    return [point for point, nlines in coverage.items() if nlines > 1]


# Example from the instructions
test_01 = '''0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2'''


if __name__ == '__main__':
    input = 'day05_input.txt'

    # Test example from the instructions
    assert len(find_intersections((parse_line_spec(row.strip()) for row in test_01.splitlines()), diagonal_allowed = False)) == 5, "Test 1 failed"
    assert len(find_intersections((parse_line_spec(row.strip()) for row in test_01.splitlines()), diagonal_allowed = True)) == 12, "Test 2 failed"

    # Run on the input
    with open(input, 'rt') as f:
        lines = [parse_line_spec(row.strip()) for row in f]
        print("Part 1:", len(find_intersections(lines, diagonal_allowed = False)))
        print("Part 2:", len(find_intersections(lines, diagonal_allowed = True)))
