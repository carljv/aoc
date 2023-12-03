def parse_pairs(fpath):
    with open(fpath, 'rt') as f:
        for row in f:
            (x1, y1), (x2, y2) = (x.split('-') for x in row.strip().split(","))
            yield (int(x1), int(y1)), (int(x2), int(y2))

# Part 1
def check_covered_pairs(pairs):
    for (x1, y1), (x2, y2) in pairs:
        if (x1 <= x2 and y1 >= y2) or (x2 <= x1 and y2 >= y1):
            yield (x1, y1), (x2, y2)

# Part 2
def check_overlapping_pairs(pairs):
    for (x1, y1), (x2, y2) in pairs:
        if (x1 <= x2 and y1 >= x2) or (x2 <= x1 and y2 >= y1) or (y1 >= y2 and x1 <= y2) or (y2 >= y1 and x2 <= y1):
            yield (x1, y1), (x2, y2)


INPUT = "day04_input.txt"

if __name__ == '__main__':
    print("Covering pairs:", len([x for x in check_covered_pairs(parse_pairs(INPUT))]))
    print("Overlapping pairs:", len([x for x in check_overlapping_pairs(parse_pairs(INPUT))]))