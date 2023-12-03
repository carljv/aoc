from  collections import Counter
from math import abs
from queue import PriorityQueue


def parse_crabs(s: str):
    '''Count how many crabs in each position.
      '''
    return Counter(int(i) for i in  s.strip().split(','))


def linear_cost(crabs, pos):
    '''Cost of moving all crabs to pos if each step costs one unit.
    '''
    return sum(abs(k - pos) * v for k, v in crabs.items())
    

def increasing_cost(crabs, pos):  
    '''Cost of moving all crabs to pos if the cost of each step increases.
    '''
    return sum(int((abs(k - pos) + 1) * (abs(k - pos)) / 2) * v for k, v in crabs.items())
    

def find_best_position(crabs, cost_fn):
    '''Given a cost function, find the lowest total cost position to 
    move all the crabs to.
    '''
    costs = PriorityQueue()
    for pos in range(max(crabs.keys())):
        costs.put((cost_fn(crabs, pos), pos))

    return costs.get(0)


# Example from the instructions
test_01 = "16,1,2,0,4,2,7,1,2,14"


if __name__ == '__main__':
    input = 'day07_input.txt'
    
    # Test example from instructions
    assert find_best_position(parse_crabs(test_01), linear_cost) == (37, 2), "Test 1 failed"
    assert find_best_position(parse_crabs(test_01), increasing_cost) == (168, 5), "Test 2 failed"

with open(input, 'rt') as f:
    crabs = parse_crabs(f.read())
    
    print('Part 1:', find_best_position(crabs, linear_cost))
    print('Part 2:', find_best_position(crabs, increasing_cost))
