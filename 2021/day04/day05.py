from collections import Counter
from itertools import zip_longest
import re
from typing import Generator, Iterable, List, Tuple

Point = Tuple[int, int]
Line = Tuple[Point, Point]


def parse_line_spec(line_spec: str) -> Tuple[Point]:
    match = re.match('^(\d)\,(\d) \-> (\d),(\d)', line_spec)
    
    try:
        x0, y0, x1, y1 = (int(i) for i in match.groups())
    except (AttributeError, ValueError):
         raise ValueError(f'Could not parse line from "{line_spec}".')

    return ((x0, y0), (x1, y1))
    

def is_sloped(line: Line) -> bool:
    x0, y0 = line[0]
    x1, y1 = line[1]

    return x0 != x1 and y0 != y1


def points_between(line: Line) -> List[Point]:
    x0, y0 = line[0]
    x1, y1 = line[1]

    assert x0 == x1 or y0 == y1, "Line is not horizontal or verticel."

    dx = 1 if x1 >= x0 else -1
    dy = 1 if y1 >= y0 else -1

    xs = list(range(x0, x1 + dx, dx))
    ys = list(range(y0, y1 + dy, dy))

    fill = x1 if len(ys) >= len(xs) else y1
        
    return list(zip_longest(xs, ys, fillvalue = fill))


def find_covered_points(lines: Iterable[Line]) -> Generator:
    for line in lines:
        if not is_sloped(line):
            for point in points_between(line):
               yield point


def find_intersections(lines: Iterable[Line]) -> List[Point]:
    coverage = Counter(find_covered_points(lines))
    return [point for point, nlines in coverage.items() if nlines > 1]




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
    input = 'day05_input.py'

    assert len(find_intersections(parse_line_spec(row.strip()) for row in test_01.splitlines())) == 5, "Test 1 failed"

    with open(input, 'rt') as f:
        print("Part 1:", len(find_intersections(parse_line_spec(row.strip()) for row in f)))