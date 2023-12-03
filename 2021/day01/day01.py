'''Advent of code 2021: Day 01
'''


def count_increases(readings: list[int]) -> int:
    '''Count how often a reading increases from the previous one.
    '''
    return len([x for x, y in zip(readings[:-1], readings[1:]) if x < y])


def count_window_increases(readings: list[int], window_len: int = 3) -> int:
    '''Calculate moving sums of readings and count how often each window 
    increases from the previous.
    '''
    windows = (readings[i:(i + window_len)] for i in range(len(readings)))
    next_windows = (readings[i:(i+ window_len)] for i in range(1, len(readings)))

    increasing_windows = (x for x, y in zip(windows, next_windows) 
                          if sum(x) < sum(y) and len(x) == window_len and len(y) == window_len)
    
    return len(list(increasing_windows))


# Example from the instructions
test_01 = """199
200
208
210
200
207
240
269
260
263
"""


if __name__ == '__main__':
    input = 'day01_input.txt'
    
    # Test instruction example
    assert count_increases([int(r) for r in test_01.splitlines()]) == 7, "Test 1 failed"
    assert count_window_increases([int(r) for r in test_01.splitlines()]) == 5, "Test 2 failed"
    # Run on input
    with open(input, 'rt') as f:
        readings = [int(row.strip()) for row in f]
        print('Part 1:', count_increases(readings))
        print('Part 1:', count_window_increases(readings))



