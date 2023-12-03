
def sum_calories_per_elf(fpath):
	n = 0
	cals_i = 0
	cal_lst = []
	with open(fpath, 'rt') as f:
		for row in f:
			try: 
				cals_i += float(row)
			except ValueError as e:
				cal_lst.append((n, cals_i))
				cals_i = 0
				n += 1
				
	return sorted(cal_lst, key = lambda x: x[1], reverse = True)



INPUT = 'day01_input.txt'

if __name__ == '__main__':
	res = sum_calories_per_elf(INPUT)
	top1 = res[0][1]
	top3 = sum(x[1] for x in res[0:3])

	print("Top elf calories:", top1)
	print("Top 3 elves calories", top3)