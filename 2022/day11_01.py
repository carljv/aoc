from collections import deque, namedtuple
from dataclasses import dataclass
import math
import re
from typing import Deque


@dataclass
class Monkey:
    id: int
    items: Deque[int]
    operation: str
    divisor: int
    true_throw: int
    false_throw: int
    inspect_times:int = 0

    def inspect_next_item(self, div = None, mod = None):
        item = self.items.pop()
       
        inspect_worry = eval(re.sub('old', str(item), self.operation))      
        if div:
            bored_worry = inspect_worry // div
        elif mod:
            bored_worry = inspect_worry % mod
        else:
            bored_worred = inspect_worry

        condition = bored_worry % self.divisor == 0
        throw_to = self.true_throw if condition else self.false_throw
        self.inspect_times += 1
        return (bored_worry, throw_to)
    
    def throw_next_item(self, monkeys, div = None, mod = None):
        item, throw_to = self.inspect_next_item(div, mod)
        other = monkeys[throw_to]
        other.items.appendleft(item)
        return None

def create_monkeys_from_commands(fpath):
    monkeys = []
    commands = []
    with open(fpath, 'rt') as f:
        for row in f:
            if len(row.strip()) > 0:
                commands.append(row.strip())
            else:
                monkeys.append(create_monkey(commands))
                commands = []
        else:
            monkeys.append(create_monkey(commands))
            commands = []
            
    return monkeys

def create_monkey(commands):
    id = re.match(r"Monkey (?P<id>\d+):", commands[0])['id']
    items = re.match(r"^Starting items: (?P<items>.*)$", commands[1])['items']
    operation = re.match(r"^Operation: new = (?P<op>.*)$", commands[2])['op']
    divisor = re.match(r"^Test: divisible by (?P<div>\d+)", commands[3])['div']
    true_throw = re.match(r"^If true: throw to monkey (?P<true>\d+)$", commands[4])['true']
    false_throw = re.match(r"^If false: throw to monkey (?P<false>\d+)$", commands[5])['false']

    return Monkey(int(id), parse_items(items), operation, int(divisor), int(true_throw), int(false_throw))

def parse_items(items):
    return deque([int(i) for i in items.split(", ")])


def compute_monkey_business(monkeys):
    activity = (m.inspect_times for m in monkeys)
    return math.prod(sorted(activity, reverse = True)[:2])


INPUT = "day11_input.txt"

if __name__ == '__main__':
    # Part 1
    monkeys = create_monkeys_from_commands(INPUT)

    nrounds = 20
    for _ in range(nrounds):
        for monkey in monkeys:
            while(monkey.items):
                monkey.throw_next_item(monkeys, div = 3)

    for m in monkeys:
        print(m.id, m.inspect_times)

    print(compute_monkey_business(monkeys)) # 120056

    # Part 2
    monkeys = create_monkeys_from_commands(INPUT)

    nrounds = 10000
    mod_reduction = math.prod(m.divisor for m in monkeys)

    for r in range(nrounds):
        for monkey in monkeys:
            while(monkey.items):
                monkey.throw_next_item(monkeys, mod = mod_reduction)

    for m in monkeys:
        print(m.id, m.inspect_times)

    print(compute_monkey_business(monkeys))


