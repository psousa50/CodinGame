import sys
import math
from collections import namedtuple
from tabnanny import check

from inputs import input

num_of_laps = 3

Point = namedtuple("Point", ["x", "y"])


def distance(p1: Point, p2: Point):
    return math.sqrt((p2.x - p1.x) * (p2.x - p1.x) + (p2.y - p1.y) * (p2.y - p1.y))


checkpoints = []

lap = 1
last_check_point = None
is_last_check_point = False
game_counter = 0
checkpoint_far_away = None
while True:
    x, y, next_checkpoint_x, next_checkpoint_y, next_checkpoint_dist, next_checkpoint_angle = [
        int(i) for i in input().split()
    ]
    if x < 0:
        print(checkpoints, file=sys.stderr, flush=True)
        break
    opponent_x, opponent_y = [int(i) for i in input().split()]

    game_counter += 1
    checkpoint = Point(next_checkpoint_x, next_checkpoint_y)

    new_checkpoint = last_check_point is None or last_check_point != checkpoint
    going_home = False
    if new_checkpoint:
        if not checkpoint in checkpoints:
            checkpoints.append(checkpoint)
        else:
            if checkpoint == checkpoints[1]:
                lap += 1
        last_check_point = checkpoint
    is_last_lap = lap == 3
    longest_path = 0
    if lap > 1 and checkpoint_far_away is None:
        for i, c in enumerate(checkpoints[1:]):
            d = distance(checkpoints[i - 1], checkpoints[i])
            if d > longest_path:
                longest_path = d
                checkpoint_far_away = c

    boost = lap == 3 and checkpoint_far_away is not None and checkpoint == checkpoint_far_away

    if next_checkpoint_angle > 90 or next_checkpoint_angle < -90:
        thrust = 0
    else:
        thrust = 100
    print(
        f"{lap} {checkpoint_far_away} {next_checkpoint_angle}",
        file=sys.stderr,
        flush=True,
    )
    if abs(next_checkpoint_angle) < 1 and boost:
        print(f"{next_checkpoint_x} {next_checkpoint_y} BOOST")
    else:
        print(f"{next_checkpoint_x} {next_checkpoint_y} {thrust}")
