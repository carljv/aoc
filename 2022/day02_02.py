# A = Rock, B = Paper, C = Scissors

RESULT_SCORE = {'WIN': 6, 'LOSS': 0, 'DRAW': 3}

PLAY_SCORES = {'A': 1, 'B': 2, 'C': 3}

RESULT_CODES = {'X': 'LOSS', 'Y': 'DRAW', 'Z': 'WIN'}

GAME_RESULT = \
{'A': {'A': 'DRAW', 'B': 'WIN',  'C': 'LOSS'}, 
 'B': {'A': 'LOSS', 'B': 'DRAW', 'C': 'WIN'}, 
 'C': {'A': 'WIN',  'B': 'LOSS', 'C': 'DRAW'}}

RESULTS_PLAYS = {opp: {res: slf for slf, res in res_map.items()} for opp, res_map in GAME_RESULT.items()}

def compute_score(opp, slf):
	return PLAY_SCORES[slf] + RESULT_SCORE[GAME_RESULT[opp][slf]]

def parse_plays_from_file(fpath):
	with open(fpath, 'rt') as f:
		for row in f:
			opp, res_code = row.split()
			res = RESULT_CODES[res_code]
			yield (opp, RESULTS_PLAYS[opp][res])
			
def total_strategy_score(plays):
	return sum(compute_score(i, j) for i, j in plays)
``
INPUT = 'day02_input.txt'

if __name__ == '__main__':
	print(total_strategy_score(parse_plays_from_file(INPUT)))
			

			