import pygame
import random
import math
from typing import List, Tuple
from collections import deque
from numpy.random import choice

from Rectangle import Rectangle

# TODO, have these on a constant file.
CENTER = (600, 350)
points = (CENTER, (0, 0), (1200, 0), (1200, 700), (0, 700))


# Returns the Euclidean distance between two points.
def L2(a: Tuple[int, int], b: Tuple[int, int]) -> float:
    return math.sqrt(math.pow((a[0]-b[0]), 2) + math.pow((a[1]-b[1]), 2))


# Returns the L infinite between two points.
# L infinite is commonly the max, not the min.
def Linf(a: Tuple[int, int], b: Tuple[int, int]) -> int:
    return min(abs(a[0]-b[0]), abs(a[1]-b[1]))


# Returns the closest corner L2 distance between two Rectangles.
def closest_L2(a: Rectangle, b: Rectangle) -> float:
    a_corners = a.get_corners()
    b_corners = b.get_corners()

    minimum = 10000
    for first in a_corners:
        for second in b_corners:
            current = L2(first, second)
            minimum = min(current, minimum)
    return minimum


# Returns the closest corner Linf distance between two Rectangles.
def closest_Linf(a: Rectangle, b: Rectangle) -> int:
    a_corners = a.get_corners()
    b_corners = b.get_corners()

    minimum = 10000
    for first in a_corners:
        for second in b_corners:
            current = Linf(first, second)
            minimum = min(current, minimum)
    return minimum


# Returns the closest rectangle to a in L2 distance.
def closest_of_all_L2(a: Rectangle, bs: List[Rectangle]) -> Rectangle:
    closest_d = 10000
    closest = bs[0]
    for b in bs:
        current_d = closest_L2(a, b)
        if current_d < closest_d:
            closest_d = current_d
            closest = b
    return closest


# Returns the closest rectangle to a in Linf distance.
def closest_of_all_Linf(a: Rectangle, bs: List[Rectangle]) -> Rectangle:
    closest_d = 10000
    closest = bs[0]
    for b in bs:
        current_d = closest_Linf(a, b)
        if current_d < closest_d:
            closest_d = current_d
            closest = b
    return closest


# Returns the direction [dx, dy] from point a to point b.
def direction_to_point(a: Tuple[int, int],
                       b: Tuple[int, int]) -> Tuple[float, float]:
    move_x = b[0] - a[0]
    move_y = b[1] - a[1]
    total = abs(move_x) + abs(move_y)

    if total == 0:
        return (0, 0)
    move_x = float(move_x) / float(total)
    move_y = float(move_y) / float(total)

    return move_x, move_y


# Returns the direction [dx, dy] from object a to object b.
# If it's not within the sensing radius r, it returns a random movement.
def sensing_direction(a: Rectangle, b: Rectangle, r: int) -> \
        Tuple[float, float]:
    a_center = a.get_center()
    corners = b.get_corners()
    for corner in corners:
        if r < L2(a_center, corner):
            return get_weighted_random_move(a.get_center(), a.get_direction())

    return direction_to_point(a_center, b.get_center())


def cardinal_system_direction(a: Rectangle, b: Rectangle) -> Tuple[int, int]:
    corners = b.get_corners()
    vip = a.get_corners()
    vip = vip[0]

    right = 0
    left = 0
    down = 0
    up = 0
    for corner in corners:
        if vip[0] <= corner[0]:
            right += 1
        if vip[0] >= corner[0]:
            left += 1
        if vip[1] <= corner[1]:
            down += 1
        if vip[1] >= corner[1]:
            up += 1

    if right == 4:
        return (1, 0)
    elif left == 4:
        return (-1, 0)
    elif down == 4:
        return (0, 1)
    elif up == 4:
        return (0, -1)
    return get_weighted_random_move(a.get_center(), a.get_direction())


# Returns the index of which direction is the optimal to go.
# 0 = up, 1 = up-right
# 2 = right, 3 = down-right
# 4 = down, 5 = down-left
# 6 = left, 7 = up-left
def index_direction_to_point(a: Tuple[int, int],
                             b: Tuple[int, int]) -> int:
    dx, dy = direction_to_point(a, b)
    if -0.25 < dx <= 0.25:  # This means dx = 0 or does not move in x.
        if dy > 0:  # It should go down.
            return 4
        else:  # It should go up.
            return 0
    elif 0.25 < dx <= 0.75:  # This means dx = 0.5 or goes right.
        if dy > 0:  # It should go down.
            return 3
        else:  # It should go up.
            return 1
    elif -0.75 < dx <= -0.25:  # This means dx = -0.5 or goes left.
        if dy > 0:  # It should go down.
            return 5
        else:  # It should go up.
            return 7
    elif 0.75 < dx:  # This means dx = 1 or goes completely right.
        return 2
    else:  # This means dx = -1 or goes completely left.
        return 6


# Returns a random weighted movement towards the direction.
def get_weighted_random_move(a: Tuple[int, int],
                             direction: int) -> Tuple[float, float]:

    possible_moves = [(0, -1), (0.5, -0.5),
                      (1, 0), (0.5, 0.5),
                      (0, 1), (-0.5, 0.5),
                      (-1, 0), (-0.5, -0.5)]
    possible_indexes = range(8)
    index = index_direction_to_point(a, points[direction])
    probabilities = [0.4, 0.2, 0.1, 0, 0, 0, 0.1, 0.2]
    probabilities = deque(probabilities)
    probabilities.rotate(index)
    index = choice(possible_indexes, 1, False, probabilities)
    return possible_moves[index[0]]
