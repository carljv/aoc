

def find_sack_shared_item(contents: str) -> str:
    if len(contents) / 2 != int(len(contents) / 2):
        raise ValueError(f"Odd number of contents in sack: {contents}, {len(contents)}")

    compartment_1 = contents[:int(len(contents) / 2)]
    compartment_2 = contents[int(len(contents) / 2):]
    shared = set(compartment_1).intersection(compartment_2)
    
    if len(shared) > 1:
        raise ValueError(f"Expected only one shared item in contents, but got {shared}.")
    
    return list(shared)[0]

PRIORITIES = {chr(i): i - 97 + 1 for i in range(97, 97 + 26)} | {chr(i): i - 65 + 27 for i in range(65, 65 + 26)}

def sack_priorities(fpath: str) -> float:
    with open(fpath, 'rt') as f:
        for row in f:
            yield PRIORITIES[find_sack_shared_item(row.strip())]

INPUT = 'day03_input.txt'

if __name__ == '__main__':
    print(sum(sack_priorities(INPUT)))
