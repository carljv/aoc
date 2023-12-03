# Opponent: A = Rock, B = Paper, C = Scissors
# Self: X = Rock, Y = Paper, X = Scissors

RESULT_SCORE = {'WIN': 6, 'LOSS': 0, 'DRAW': 3}

PLAY_SCORES = {'X': 1, 'Y': 2, 'Z': 3}

GAME_RESULT = \
{'A': {'X': 'DRAW', 'Y': 'WIN',  'Z': 'LOSS'}, 
 'B': {'X': 'LOSS', 'Y': 'DRAW', 'Z': 'WIN'}, 
 'C': {'X': 'WIN',  'Y': 'LOSS', 'Z': 'DRAW'}}


def compute_score(opp, slf):
	return PLAY_SCORES[slf] + RESULT_SCORE[GAME_RESULT[opp][slf]]

def parse_plays_from_file(fpath):
	with open(fpath, 'rt') as f:
		for row in f:
			yield row.split()

def total_strategy_score(plays):
	return sum(compute_score(i, j) for i, j in plays)

INPUT = 'day02_input.txt'

if __name__ == '__main__':
	print(total_strategy_score(parse_plays_from_file(INPUT)))
	