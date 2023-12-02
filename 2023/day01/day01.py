import re
from typing import Callable, Iterable

# A function that takes a line of text and extracts and parses digits from it.
DigitParser = Callable[[str], Iterable[int]]


def parse_numeric_digits(line:str) -> list[int]:
    '''Extract and parse all instances 0-9 in a string.
    '''
    return [int(x) for x in line if x.isdigit()]


def parse_numeric_and_word_digits(line: str) -> list[int]:
    '''Extract all instances of 0-9 and English words for single digits in a string, and parse them to integers.

    When digit words overlap ("nineighttwo") they are all parsed (9, 8, 2).
    '''
    word_digits = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
    digit_pattern = re.compile(r'(?=(\d{1}|' + '|'.join(word_digits) + '))')
    return [int(x) if x.isdigit() else word_digits.index(x) for x in re.findall(digit_pattern, line)]
    

def combine_digits(digits: Iterable[int]) -> int:
    '''Combine the first and last digit in a list into a two digit number.

    If the list only has one digit then then repeat it twice: [3] -> 33. An empty list returns zero.
    '''
    return int(str(digits[0]) + str(digits[-1])) if digits else 0


def decode_calibration_document(input: Iterable, digit_parser: DigitParser) -> int:
    '''Read in a calibration document from a file and parse the lines to decode it.
    '''
    return sum(combine_digits(digit_parser(line)) for line in input)


# Instruction examples
test_01 = """1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet""".splitlines()

test_02 = """two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen""".splitlines()

# Input
input_file = 'day01_input.txt'

if __name__ == '__main__':
    # Test instruction examples
    assert decode_calibration_document(test_01, parse_numeric_digits) == 142, "Test 1 failed"
    assert decode_calibration_document(test_02, parse_numeric_and_word_digits) == 281, "Test 2 failed"

    # Run on input
    with open(input_file, 'rt') as f:
        print('Part 1:', decode_calibration_document(f, parse_numeric_digits))
    
    with open(input_file, 'rt') as f:
        print('Part 2:', decode_calibration_document(f, parse_numeric_and_word_digits))
