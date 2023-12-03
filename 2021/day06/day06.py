from collections import Counter, defaultdict
from typing import Dict

# A school of lanternfish
School = Dict[int, int]


def next_day_school(school: School) -> School:
    '''Update a school of fish after one day.
    '''
    updated = defaultdict(lambda : 0)

    updated[8] = school[0]
    
    for i in range(8):
        updated[i] = school[i + 1]

    updated[6] += school[0]

    return updated


def update_school(ndays: int, initial_school: School) -> School:
    '''Update a school of fish over a number of days.
    '''
    school = initial_school
    for _ in range(ndays):
        school = next_day_school(school)

    return school


def count_fish(school: School) -> int:
    '''Count the number of fish in a school.
    '''
    return sum(school.values())

def parse_school(s: str) -> School:
    '''Create a school of lanternfish from a string.
    '''
    return Counter(int(i) for i in s.strip().split(','))

# Example from the instructions
test_01 = "3,4,3,1,2"

if __name__ == '__main__':
    input = 'day06_input.txt'

    # Test the example from the instructions
    assert count_fish(update_school(80, parse_school(test_01))) == 5934, "Test 1 failed"
    assert count_fish(update_school(256, parse_school(test_01))) == 26984457539, "Test 2 failed"

    # Run on the input
    with open(input, 'rt') as f:
        school = parse_school(f.read())
        print('Part 1:', count_fish(update_school(80, school)))
        print('Part 2:', count_fish(update_school(256, school)))
