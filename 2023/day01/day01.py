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


def decode_calibration_document(input: str, digit_parser: DigitParser) -> int:
    '''Read in a calibration document from a file and parse the lines to decode it.
    '''
    with open(input, 'rt') as f:
        return sum(combine_digits(digit_parser(line)) for line in f)


if __name__ == '__main__':
   # Test instruction examples
   assert(decode_calibration_document('day01_test01.txt', parse_numeric_digits) == 142)
   assert(decode_calibration_document('day01_test02.txt', parse_numeric_and_word_digits) == 281)

    # Run on input
   print('Part 1:', decode_calibration_document('day01_input.txt', parse_numeric_digits))
   print('Part 2:', decode_calibration_document('day01_input.txt', parse_numeric_and_word_digits))
