from typing import Iterable, List, NamedTuple
import re


class Draw(NamedTuple):
    red: int
    green: int
    blue: int

class Game(NamedTuple):
    id: int
    draws: List[Draw]

class Bag(NamedTuple):
    red: int
    green: int
    blue: int
    

def parse_game(game: str) -> Game:
    '''Create an instance of a game from a string.
    '''
    game_name, draws = re.split(r':', game)
    game_id = int(re.search(r'\d+$', game_name)[0])
    draws = [parse_draw(x) for x in re.split(r';', draws)]

    return Game(game_id, draws)


def parse_draw(draw: str) -> Draw:
    '''Create an instance of a Draw from a string by finding the number of red,
    green, and blue cubes.
    
    If a color isn't present in the string, it means zero cubes of that color
    were drawn.
    '''
    red = int((re.search(r'\d+(?=\s+red)', draw) or ['0'])[0])
    green =  int((re.search(r'\d+(?=\s+green)', draw) or ['0'])[0])
    blue =  int((re.search(r'\d+(?=\s+blue)', draw) or ['0'])[0])
    return Draw(red, green, blue)


def is_draw_possible(draw: Draw, bag: Bag) -> bool:
    '''Could a draw have been made from a bag?

    A draw is possible if the number of each color cube is no more than what's 
    in the bag.
    '''
    return draw.red <= bag.red and draw.green <= bag.green and draw.blue <= bag.blue


def is_game_possible(game: Game, bag: Bag) -> bool:
    '''Could all the draws from a game have been made from a bag?
    '''
    return all(is_draw_possible(d, bag) for d in game.draws)


def possible_games(games: Iterable[Game], bag: Bag) -> List[int]:
    '''Given a list of games and a bag, which games could have been played from 
    the bag?
    '''
    return [game.id for game in games if is_game_possible(game, bag)]


def minimum_bag(game: Game) -> Bag:
    '''Given the draws in a game, what is the fewest number of each cube that 
    could be in the bag?
    '''
    min_red = max(d.red for d in game.draws)
    min_green = max(d.green for d in game.draws)
    min_blue = max(d.blue for d in game.draws)

    return Bag(min_red, min_green, min_blue)


def bag_power(bag: Bag) -> int:
    '''The power set of a bag is just the product of its contents.'''
    return bag.red * bag.green * bag.blue


# Example from instructions
test_01 = """Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
"""


if __name__ == '__main__':
    input = 'day02_input.txt'

    bag = Bag(red = 12, green = 13, blue = 14)

    # Test examples from instructions
    assert possible_games([parse_game(g) for g in test_01.splitlines()], bag) == [1, 2, 5], "Test 1 failed"
    assert sum(bag_power(b) for b in (minimum_bag(parse_game(g)) for g in test_01.splitlines())) == 2286, "Test 2 failed"

    # Run on input
    with open(input, 'rt') as f:
        games = [parse_game(row.strip()) for row in  f]
        minimum_bags = [minimum_bag(g) for g in games]
        print('Part 1:', sum(possible_games(games, bag)))
        print('Part 2:', sum(bag_power(b) for b in minimum_bags))
    
    

