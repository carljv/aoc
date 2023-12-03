'''Advent of Code 2021: Day 04
'''

from dataclasses import dataclass, field
from typing import List, Set, Tuple

@dataclass
class Player:
    card: List[List[int]]
    marks: Set[Tuple[int, int]] = field(default_factory = lambda: set([]))

    def mark_card(self, number):
        for i, row in enumerate(self.card):
            if number in row:
                self.marks.add((i, row.index(number)))
        else:
            return None

    def check_win(self):
        row_idxs = list(range(5))
        
        # diag1_marks = len(self.marks.intersection(set((i, i) for i in row_idxs)))
        # diag2_marks = len(self.marks.intersection(set((i, j) for i, j in zip(row_idxs, row_idxs[::-1]))))

        row_marks = max(sum(1 for m in self.marks if m[0] == i) for i in row_idxs)
        col_marks = max(sum(1 for m in self.marks if m[1] == i) for i in row_idxs)

        return row_marks == 5 or col_marks == 5
        
    def unmarked(self):
        row_idxs = list(range(5))
        return set((i, j) for i in row_idxs for j in row_idxs).difference(self.marks)


@dataclass
class Game:
    draws: List[int]
    players: List[Player]


def parse_bingo_game(s: str) -> Game:
    '''Create an instance of a bingo game from a string.
    
    A game is a list of numbers drawn and a list of players with bingo cards.
    '''
    lines = s.splitlines()

    draws = [int(i) for i in lines[0].strip().split(',')]
    cards = [[]]

    for line in lines[1:]:
        if len(cards[-1]) >= 5:
            cards.append([])
        if line.strip():
            cards[-1].append([int(i) for i in line.split()])

    return Game(draws, [Player(card = c) for c in cards])


def play_game(game: Game) -> Tuple[int, Player] | None:
    '''Play bingo.
    
    Keep drawing until somebody wins. Identify the winner and the draw that ended the game.
    
    Returns None if there are no winners.
    '''
    for draw in game.draws:
        for player in game.players:
            player.mark_card(draw)
            if player.check_win():
                return draw, player
    else:
        return None


def play_squid_game(game: Game) -> Tuple[int, Player] | None:
    '''Play bingo, letting the squid win.
    
    Keep drawing until every card wins. Identify the draw that ended the game and the last winner.
    
    Returns none if there are no winners.'''
    for draw in game.draws:
        for player in game.players:
            player.mark_card(draw)
            if all(p.check_win() for p in game.players):
                return draw, player
    else:
        return None


def play_and_summarize_game(game: Game, has_squid: bool = False) -> int:
    '''Play a game of bingo and summarize the result. 
    
    The summary is the the winning draw times the sum unmarked values on the winner's card.

    Play a normal game by default, unless there's a squid.
    '''
    if not has_squid:
        result = play_game(game)
    else:
        result = play_squid_game(game)

    if result:
        draw, winner = result
        total_unmarked = sum(winner.card[i][j] for i, j in winner.unmarked())
        return total_unmarked * draw
    else:
        return 0


test_01 = '''7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7
'''


if __name__ == '__main__':
    input = "day04_input.py"

    # Test the example from the instructions
    assert play_and_summarize_game(parse_bingo_game(test_01)) == 4512, "Test 1 failed"
    assert play_and_summarize_game(parse_bingo_game(test_01), has_squid = True) == 1924, "Test 2 failed"

    # Run on input
    with open(input, 'rt') as f:
        game = parse_bingo_game(f.read())
        print('Part 1:', play_and_summarize_game(game))
        print('Part 2:', play_and_summarize_game(game, has_squid = True))