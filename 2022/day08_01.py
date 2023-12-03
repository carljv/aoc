from typing import Iterable
import numpy as np

def read_map(fpath):
    with open(fpath, 'rt') as f:
        return np.array([[int(x) for x in row.strip()] for row in f])
    

def find_visible_trees(map):
   
    visible_trees = []
    for i in range(map.shape[0]):
        for j in range(map.shape[1]):
            height = map[i, j]
            tallest_left = np.max(map[i, :j], initial = -1)
            tallest_right = np.max(map[i, (j+1):], initial = -1)
            tallest_up = np.max(map[:i, j], initial = -1)
            tallest_down = np.max(map[(i+1):, j], initial = -1)

            if min([tallest_left, tallest_right, tallest_up, tallest_down]) < height:
                visible_trees.append((i, j))

    return visible_trees

def first_n_shorter(x: int, xs: Iterable[int]) -> int:
    if len(xs) <= 0:
        return 0
    
    for i, xi in enumerate(xs):
        if xi >= x:
            break
    return i + 1

def compute_view_areas(map):
    view_areas = np.empty_like(map)

    for i in range(map.shape[0]):
        for j in range(map.shape[1]):
            height = map[i, j]
            view_left = first_n_shorter(height, map[i, :j][::-1])
            view_right = first_n_shorter(height, map[i, (j+1):])
            view_up = first_n_shorter(height, map[:i, j, ][::-1])
            view_down = first_n_shorter(height, map[(i+1):, j])
            view_areas[i, j] = view_left * view_right * view_up * view_down

    return view_areas

INPUT = 'day08_input.txt'

if __name__ == '__main__':
    map = read_map(INPUT)
    visible_trees = find_visible_trees(map)
    print("01. Visible trees:", len(visible_trees)) # 1698
    view_areas = compute_view_areas(map)
    print("02. Maximum view area:", np.max(view_areas)) # 672280