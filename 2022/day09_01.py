from collections import deque, namedtuple
import re

def move_tail(head_coords, tail_coords):
    xh, yh = head_coords
    xt, yt = tail_coords

    dx = xh - xt
    dy = yh - yt
    dirx = dx / abs(dx) if abs(dx) > 0 else 0
    diry = dy / abs(dy) if abs(dy) > 0 else 0
    
    # No need to move
    if abs(dx) <= 1 and abs(dy) <= 1:
        return (xt, yt)
    # Move vertically
    elif abs(dx) == 0 and abs(dy) > 1:
        return (xt, yt + diry)
    # Move horizontally
    elif abs(dx) > 1 and abs(dy) == 0:
        return (xt + dirx, yt)
    # Move diagonally
    elif abs(dx) == 1 and abs(dy) > 1:
        return (xt + dirx, yt + diry)
    elif abs(dx) > 1 and abs(dy) == 1:
        return (xt + dirx, yt + diry)
    elif abs(dx) > 1 and abs(dy) > 1:
        return (xt + dirx, yt + diry)
    else:
        raise ValueError(f"Head and tail in illegal positions {head_coords} and {tail_coords}.")
    
def move_head(head_coords, dirs):
    x, y = head_coords
    dx, dy = dirs
    return (x + dx, y + dy)

Movement = namedtuple('Movement', ['dirs', 'n'])

def parse_movement(cmd):
    cmd_match = re.match("^(?P<dir>[UDLR]{1})\s+(?P<n>\d+)$", cmd)
    
    dir_map = {'U': (0, 1), 'D': (0, -1), 'L': (-1, 0), 'R': (1, 0)}

    return Movement(dirs = dir_map[cmd_match['dir']], n = int(cmd_match['n']))
 
    
INPUT = 'day09_input.txt'

def read_movements_from_input(fpath):
    with open(fpath, 'rt') as f:
        return [parse_movement(cmd.strip()) for cmd in f]
    
def move_rope(head_coords, tail_coords, mvmt):
    for i in range(mvmt.n):
        head_coords = move_head(head_coords, mvmt.dirs)
        tail_coords = move_tail(head_coords, tail_coords)

    return (head_coords, tail_coords)

def trace_movements(nknots, movements, init_coords = (0, 0)):
    coord_traces = [[init_coords] for _ in range(nknots)]

    for movement in movements:
        for i in range(movement.n):
            head_coords = move_head(coord_traces[0][-1], movement.dirs)
            coord_traces[0].append(head_coords)
            for k in range(1, nknots):
                tail_coords = move_tail(coord_traces[k - 1][-1], coord_traces[k][-1])
                coord_traces[k].append(tail_coords)

    return coord_traces


if __name__ == '__main__':
    movements = read_movements_from_input(INPUT)
    res1 = trace_movements(2, movements)
    print(len(set(res1[-1]))) # 6745
    res2 = trace_movements(10, movements)
    print(len(set(res2[-1]))) # 2793