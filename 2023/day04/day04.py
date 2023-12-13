'''Advent of Code 2023: Day 04
'''

import re
from typing import List, NamedTuple, FrozenSet

class Card(NamedTuple):
    card_id: int
    winning_numbers: FrozenSet[int]
    held_numbers: List[int]


def parse_card(s: str) -> Card:
    '''Create an instance of a card from a string.

    A card has an ID, a list of winning numbers and a list of numbers "held."
    '''
    id_str, winning_str, held_str = re.split(r'[:|]', s)
    card_id = int(re.search('\d+$', id_str.strip())[0])
    winning_numbers = frozenset(int(i) for i in winning_str.split())
    held_numbers = [int(i) for i in held_str.split()]
    return Card(card_id, winning_numbers, held_numbers)

def find_matches(card: Card) -> int:
    """Find the number of matches on a card.
    
    A match occurs when a number "held" is amongst the list of winning numbers.
    """
    return sum(1 for n in card.held_numbers if n in card.winning_numbers)


def score_card(card: Card) -> int:
    """Score a card based on its matches.

    The score starts at 1 for the first match and doubles for every
    subsequent match. 
    """
    n_matches = find_matches(card)
    return 2**(n_matches - 1) if n_matches > 0 else 0


def count_cards_won(cards: List[Card]) -> List[int]:
    """Determine copies of cards one from a given pile of cards.
    
    Whenever a card has matches, we win copies of the cards after it
    up to the number of matches.
    """

    counts = [1 for _ in cards]

    for i, card in enumerate(cards):
        n_matches = find_matches(card)
        # Iterate over the copies we've won of this card
        for _ in range(counts[i]):
            # Win copies of subesequent cards
            for j in range(1, n_matches + 1):
                counts[i + j] += 1

    return counts


# Example from the instructions
test_01 = '''Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
'''


if __name__ == '__main__':
    input = 'day04_input.py'

    # Test example from instructions
    assert sum(score_card(parse_card(row)) for row in test_01.splitlines()) == 13, "Test 1 failed."
    assert sum(count_cards_won([parse_card(row) for row in test_01.splitlines()])) == 30, "Test 2 failed."

    # Run on input
    with open(input, 'rt') as f:
        cards = [parse_card(row) for row in f.read().splitlines()]
        print('Part 1:', sum(score_card(card) for card in cards))
        print('Part 2:', sum(count_cards_won(cards)))