'''Advent of Code 2021: Day 03
'''

from collections import Counter
from typing import Callable, List

Report = List[str]
BitFilter = Callable[[Report], str]


def most_common_bits(report: Report) -> str:
    '''Find the most common bit of each digit in a report of binary numbers.
    '''
    counters = []
    for row in report:
        for i, digit in enumerate(row):
            try:
                counters[i].update(digit)
            except IndexError:
                counters.append(Counter())
                counters[i].update(digit)

    return ''.join('1' if c['1'] >= c['0'] else '0' for c in counters)


def flip_bits(bits: str) -> str:
    '''Flip each bit in a string of bits.
    '''
    flip_bit = {'0': '1',  '1': '0'}
    return ''.join(flip_bit[bit] for bit in bits)


def least_common_bits(report: Report) -> str:
    '''Find the least common bit of each digit in a report of binary numbers.
    '''
    return flip_bits(most_common_bits(report))


def compute_power(report: Report) -> int:
    '''Compute the sub's power using a report of binary numbers.
    '''
    mcb = most_common_bits(report)
    lcb = flip_bits(mcb)
    gamma = int(mcb, base = 2)
    epsilon = int(lcb, base = 2)

    return gamma * epsilon


def apply_bit_filter(report: Report, bit_filter: BitFilter) -> str:
    '''Filter a report to a single number by successively applying a bitstring filter.
    '''
    remaining_rows = report
    
    digit = 0
    while len(remaining_rows) > 1:
        bits = bit_filter(remaining_rows)
        remaining_rows = [row for row in remaining_rows if row[digit] == bits[digit]]
        digit += 1

    return remaining_rows[0]        


def compute_oxygen_rating(report: Report) -> int:
    '''Filter a report to find the oxygen rating.
    '''
    return int(apply_bit_filter(report, most_common_bits), base = 2)


def compute_co2_scrubber_rating(report: Report) -> int:
    '''Filter a report to find the CO2 scrubber rating.
    '''
    return int(apply_bit_filter(report, least_common_bits), base = 2)


def compute_life_support_rating(report: Report) -> int:
    '''The life support rating is the product of the oxygen and CO2 scrubber ratings.
    '''
    return compute_co2_scrubber_rating(report) * compute_oxygen_rating(report)


# Example from the instructions
test_01 = '''00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010'''


if __name__ == '__main__':
    input = 'day03_input.txt'

    # Test example from instructions
    assert compute_power([row.strip() for row in test_01.splitlines()]) == 198, "Test 1 failed"
    assert compute_life_support_rating([row.strip() for row in test_01.splitlines()]) == 230, "Test 2 failed"

    # Run on input
    with open(input, 'rt') as f:
        report = [row.strip() for row in f]
        print('Part 1:', compute_power(report))
        print('Part 2:', compute_life_support_rating(report))
