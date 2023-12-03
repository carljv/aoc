from collections import defaultdict
import re
from typing import List, NamedTuple, Tuple


Point = Tuple[int, int]
Schematic = List[str]


class PartNumber(NamedTuple):
    number: int
    schematic_location: Point


class Symbol(NamedTuple):
    symbol: str
    schematic_location: Point


def parse_schematic(s: str) -> Schematic:
    '''A schematic is a list of strings. Each element a row, each character a column.
    '''
    return s.splitlines()


def get_schematic_point(point: Point, schematic: Schematic) -> str:
    '''Find the character at a given point in a schematic.
    '''
    x, y = point
    return schematic[x][y]


def is_symbol(char: str) -> bool:
    '''Anything in a schematic that isn't a . or a number is a symbol.
    '''
    return not (char == '.' or char.isdigit())


def get_part_numbers(schematic: Schematic) -> List[PartNumber]:
    '''Find all the part numbers in a schematic and their location.
    
    A part number's location is the (row, column) of its first digit in
    the schematic.
    '''
    part_nos = []
    for i, row in enumerate(schematic):
        # Find all the part numbers in a row of the schematic
        row_part_nos = re.finditer('\d+', row)

        # Find the location of the part number in the row.
        # If this part number was already found in the schematic,
        # add this location to the others.
        for part_no in row_part_nos:
            part_nos.append(PartNumber(int(part_no.group()), (i, part_no.start())))
    
    return part_nos
            

def find_adjacent_points(part_no: PartNumber) -> List[Point]:
    '''Given a part number in a schematic, find all the points adjacent to the 
    part number's location.

    Points returned may extend beyond the dimensions schematic.
    '''
    row, start = part_no.schematic_location
    end = start + len(str(part_no.number))
    
    number_pts = [(row, x) for x in range(start, end)]
    bordered_rows = list(range(max(row - 1, 0), row + 2))
    bordered_cols = list(range(max(start - 1, 0), end + 1))
   
    return [(i, j) for i in bordered_rows for j in bordered_cols if (i, j) not in number_pts]


def find_adjacent_symbols(part_no: PartNumber, schematic: Schematic) -> bool:
    '''Given a part number in a schematic, find all the symbols adjacent to it
    '''
    symbols = []

    for pt in find_adjacent_points(part_no):
        try:
            char = get_schematic_point(pt, schematic)
            if is_symbol(char):
                sym = Symbol(char, pt)
                symbols.append(sym)
        except IndexError:
            pass
    
    return symbols


def summarize_schematic(schematic: Schematic) -> int:
    '''Sum up every number in the schematic that is adjacent to a symbol.

    The same number can occur more than once in a schematic. It gets added to the sum
    every time it occurs and is adjacent to a symbol.
    '''
    part_nos = get_part_numbers(schematic)
    return sum(p.number for p in part_nos if find_adjacent_symbols(p, schematic))


def summarize_gear_ratios(schematic: Schematic) -> int:
    '''Sum up the gear ratios of ecery gear in the schematic.

    A gear has the symbol "*" and is adjacent to two part numbers. The gear
    ratio of the gear is the product of the two part numbers.
    '''
    part_nos = get_part_numbers(schematic)
    gears_parts = defaultdict(list)
    
    for part_no in part_nos:
        for sym in find_adjacent_symbols(part_no, schematic):
            if sym.symbol == '*':
                gears_parts[sym].append(part_no.number)

    return sum(parts[0] * parts[1] for gear, parts in gears_parts.items() if len(parts) == 2)


# Example from the instructions
test_01 = '''467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..'''


if __name__ == '__main__':
    input = 'day03_input.txt'
    
    # Test the example from the instructions
    assert summarize_schematic(parse_schematic(test_01)) == 4361, "Test 1 failed"
    assert summarize_gear_ratios(parse_schematic(test_01)) == 467835, "Test 2 failed"
    
    # Run on input
    with open(input, 'rt') as f:
        schematic = parse_schematic(f.read())
        print('Part 1:', summarize_schematic(schematic))
        print('Part 2:', summarize_gear_ratios(schematic))
 
