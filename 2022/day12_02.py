from dataclasses import dataclass
from queue import PriorityQueue
import numpy as np
from typing import Dict, Iterable, Tuple

Coord = Tuple[int, int]
MapGraph = Dict[Coord, Iterable[Coord]]


def read_map_from_input(fpath: str) -> np.ndarray:
    with open(fpath) as f:
        return np.array([list(row.strip()) for row in f.readlines()])


def make_map_graph(map: np.ndarray, reversed = False):
    graph = {}

    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    elevation = {chr(i): i - 97 for i in range(97, 97 + 26)} | {'S': 0, 'E': 25}

    for i in range(map.shape[0]):
        for j in range(map.shape[1]):
            graph[(i, j)] = []
            for di, dj in directions:
                if 0 <= i + di < map.shape[0] and 0 <= j + dj < map.shape[1]:
                    if elevation[map[i + di, j + dj]] - elevation[map[i, j]] <= 1:
                        graph[(i, j)].append((i + di, j + dj))

    return graph




def shortest_paths(graph: MapGraph, origin: Coord) -> Dict[Coord, int]:
    distances = {n: 0 if n == origin else float('inf') for n in graph}
    unvisited = set(n for n in graph)

    while unvisited:
        closest_node, closest_distance = sorted(((k, v) for k, v in distances.items() if k in unvisited), 
                                                key = lambda x: x[1])[0]
        new_distance = closest_distance + 1
        unvisited_neighbors = unvisited.intersection(graph[closest_node])

        unvisited.remove(closest_node)

        for neighbor in unvisited_neighbors:
            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance

    return distances

INPUT = 'day12_input.txt'

if __name__ == '__main__':
    map = read_map_from_input(INPUT)
    graph = make_map_graph(map)

    origin = list(zip(*np.where(map == 'S')))
    destination = list(zip(*np.where(map == 'E')))
    elevation_a_nodes = list(zip(*np.where((map == 'a') | (map == 'S'))))

    #distances_from_origin = shortest_paths(graph, origin)

    #print('Part 1, shortest path to from S to E:', distances_from_origin[destination]) # 504

