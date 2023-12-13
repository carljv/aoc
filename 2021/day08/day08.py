

def parse_entry(entry: str):
    signal_pattern, output = entry.split('|')
    signal_patterns = [set(x.strip()) for x in signal_pattern.split()]
    outputs = [frozenset(x.strip()) for x in output.split()]
    return(signal_patterns, outputs)


def decode(patterns, output):
    decoded_digits = {}
    decoded_segments = {}

    # Decode full digits by their length
    decoded_digits[1] = [d for d in patterns if len(d) == 2][0]
    decoded_digits[4] = [d for d in patterns if len(d) == 4][0]
    decoded_digits[7] = [d for d in patterns if len(d) == 3][0]
    decoded_digits[8] = [d for d in patterns if len(d) == 7][0]

    # Decode individual segments by how many digits they appear in
    for seg in 'abcdefg':
        occurs = sum(1 for pattern in patterns if seg in pattern)
        if occurs == 9:
            decoded_segments['f'] = seg
        elif occurs == 8:
            decoded_segments['a'] = seg
        elif occurs == 6:
            decoded_segments['b'] = seg
        elif occurs == 4:
            decoded_segments['e'] = seg
        else:
            pass

    decoded_digits[2] = decoded_digits[8].difference(decoded_segments['b']).difference(decoded_segments['f'])
    decoded_digits[3] = decoded_digits[8].difference(decoded_segments['b']).difference(decoded_segments['e'])
    decoded_segments['c'] = decoded_digits[1].difference(decoded_segments['f'])
    decoded_digits[6] = decoded_digits[8].difference(decoded_segments['c'])
    decoded_digits[5] = decoded_digits[6].difference(decoded_segments['e'])
    decoded_digits[9] = decoded_digits[8].difference(decoded_segments['e'])
    decoded_segments['d'] = decoded_digits[4].difference(decoded_digits[1]).difference(decoded_segments['b'])
    decoded_digits[0] = decoded_digits[8].difference(decoded_segments['d'])

    decoder = {frozenset(segs): str(digit) for digit, segs in decoded_digits.items()}
    return int(''.join(decoder[o] for o in output))

def count_easy_digits(digits):
    return len([d for d in digits if len(d) in (2, 3, 4, 7)])
    

test_01 = '''be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce
'''


if __name__ == '__main__':
    input = 'day08_input.txt'

    assert sum(count_easy_digits(parse_entry(row)[1]) for row in test_01.splitlines()) == 26, "Test 1 failed."

    assert sum(decode(*parse_entry(row)) for row in test_01.splitlines()) == 61229, "Test 2 failed."

    with open(input, 'rt') as f:
        entries = [parse_entry(row) for row in f]
        print(sum(count_easy_digits(o) for _, o in entries))
        print(sum(decode(*e) for e in entries))
