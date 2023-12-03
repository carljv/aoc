from dataclasses import dataclass, field
import math
from queue import PriorityQueue
from os import PathLike
from pathlib import Path
from typing import Any, Dict, List, NamedTuple, Tuple, Union

import numpy as np
from numpy.typing import NDArray

Coord = Tuple[int, int]

@dataclass(frozen = True, eq = True)
class MapNode:
    coord: Coord
    elev: int
    is_start: bool
    is_end: bool
    next_steps: list[Coord]
    prev_steps: list[Coord]


@dataclass(frozen = True, eq = True)
class Map:
    _map: List[List[MapNode]] = []

    def from_string(self, s):
        string_map = [list(row) for row in s.split('\n')]
        map = []
        for x, row in enumerate(string_map):
            map_row = []
            for y, el in enumerate(row):
                map_row.append(self._make_node(string_map, (x, y)))
            map.append(map_row)
            self._map = map

    def _make_node(str_map: List[List[str]], coord: Coord) -> MapNode:
        x1, y1 = coord
        next_steps = [] 
        prev_steps = []

        directions = {'up': (0, 1), 'down': (0, -1), 'left': (-1, 0), 'right': (1, 0)}    

        for dx, dy in directions.values():
            x2 = x1 + dx
            y2 = y1 + dy
            if in_map(str_map, x2, y2) and height(map[x1, y1], map[x2, y2]) <= 1:
                next_steps.append([x2, y2])
            if in_map(map, x2, y2) and height(map[x2, y2], map[x1, y1]) <= 1:
                prev_steps.append([x2, y2])

        elev = map[x1, y1]
        elev = 'a' if elev == 'S' else elev
        elev = 'z' if elev == 'E' else elev

        is_start = map[x1, y1] == 'S'
        is_end = map[x1, y1] == 'E'
        dist_from_origin = 0 if is_start else float('inf')
        return MapNode(coord, elev, is_start, is_end, next_steps, prev_steps, dist_from_origin)



def read_map(fpath: str | PathLike) -> Tuple[Map, Coord, Coord]:
    raw_map = []
    with open(fpath) as f:
        for row in f:
            raw_map.append(list(row.strip()))
 
    parsed_map = []
    for x, row in enumerate(raw_map): 
        row = []
        for y, el in enumerate(row):
            row.append(make_node(map, (x, y)))
        parsed_map.append(row)

    return parsed_map
    

def find_start(map: Map) -> Coord:
    x, y = np.where(map == 'S')[0]
    return (x, y)

def find_end(map: Map) -> Coord:
    x, y = np.where(map == 'E')
    return (x, y)

def in_map(map: Map, coord: Coord) -> bool:
    x, y = coord
    return x >= 0 and x < map.shape[0] and y >= 0 and y < map.shape[1]


def height(from_el: str, to_el: str) -> int:
    elevations: Dict[str, int] = {chr(i): i - 97 for i in range(97, 97 + 26) } | {'S': 0, 'E': 26}
    return elevations[to_el] - elevations[from_el]


def make_node(map: Map, coord: Coord) -> MapNode:
    x1, y1 = coord
    next_steps = [] 
    prev_steps = []

    directions = {'up': (0, 1), 'down': (0, -1), 'left': (-1, 0), 'right': (1, 0)}    

    for dx, dy in directions.values():
        x2 = x1 + dx
        y2 = y1 + dy
        if in_map(map, x2, y2) and height(map[x1, y1], map[x2, y2]) <= 1:
            next_steps.append([x2, y2])
        if in_map(map, x2, y2) and height(map[x2, y2], map[x1, y1]) <= 1:
            prev_steps.append([x2, y2])

    elev = map[x1, y1]
    elev = 'a' if elev == 'S' else elev
    elev = 'z' if elev == 'E' else elev

    is_start = map[x1, y1] == 'S'
    is_end = map[x1, y1] == 'E'
    dist_from_origin = 0 if is_start else float('inf')
    return MapNode(coord, elev, is_start, is_end, next_steps, prev_steps, dist_from_origin)

def make_node_matrix(map: Map) -> np.ndarray:
    nodes = []
    for row in range(map.shape[0]):
        nodes.append([])
        for col in range(map.shape[1]):
            nodes[row].append(make_node(map, [row, col]))
    
    return np.array(nodes)

def closest_node(distances: np.ndarray, visited: np.ndarray) -> Coord:
    # Initialize minimum distance for next node
    min_val: float = float('inf')
    min_index: Coord = (0, 0)

    # Loop through all nodes to find minimum distance
    for i in range(distances.shape[0]):
        for j in range(distances.shape[1]):
            if distances[i, j] < min_val and visited[i, j] == 0:
                min_val = distances[i, j]
                min_index = (i, j)

    return min_index

def shortest_path(nodes: np.ndarray, origin: Coord, dest: Coord) -> np.ndarray:
    x0, y0 = origin
    x1, y1 = dest

    distances: np.ndarray[np.float_] = np.ones_like(nodes) * float('inf')
    distances[x0, y0] = 0
    visited: np.ndarray[np.int_] = np.zeros_like(nodes, dtype = 'int')



    for i in range(nodes.shape[0]):
        for j in range(nodes.shape[1]):
            if np.all(visited == 1): 
                return(distances)

            xi, yi = closest_node(distances, visited)
            visited[xi, yi] = 1

            for (xn, yn) in nodes[xi, yi].next_steps:
                new_distance = distances[xi, yi] + 1
                if new_distance < distances[xn, yn]:
                    distances[xn, yn] = new_distance

    return distances
        

def shortest_distances(map, origin):
    unvisited = None
    distances = None

    for node in map:
        for neighbor in node.neighbors:
            if neighbor in unvisited:
                distances[neighbor] += 1
        unvisited.remove(node)





def read_map(fpath):
    with open(fpath, 'rt') as f:
        for i, row in enumarate()


INPUT = 'day12_input.txt'

if __name__ == '__main__':
    map, origin, dest = read_map(INPUT)

    nodes = make_node_matrix(map)

    #ds = shortest_path(nodes, origin, dest)
    #print(ds[dest[0], dest[1]]) # 504



   
