from copy import deepcopy
from dataclasses import dataclass
from dis import dis
import sys
from collections import namedtuple
import math
import functools
from turtle import position

from inputs import input

sign = functools.partial(math.copysign, 1)


def read_input():
    inputs_line = input()
    # print(inputs_line, file=sys.stderr, flush=True)
    return inputs_line


Point = namedtuple("Point", ["x", "y"])


@dataclass()
class Entity:
    id: int
    type: int
    position: Point
    shield_life: int
    is_controlled: int
    health: int
    direction: Point
    near_base: int
    threat_for: int
    threat: bool
    distance_to_base: int
    monster_to_attack: "Entity"


TYPE_MONSTER = 0
TYPE_MY_HERO = 1
TYPE_OP_HERO = 2

MAX_WIDTH = 17630
MAX_HEIGHT = 9000
BASE_RADIUS = 5000


def on_screen(p: Point):
    return p.x > 0 and p.x < MAX_WIDTH and p.y > 0 and p.y < MAX_HEIGHT


def distance(p1: Point, p2: Point):
    return math.sqrt((p2.x - p1.x) * (p2.x - p1.x) + (p2.y - p1.y) * (p2.y - p1.y))


def intercept_with_base(monster):
    # if monster.id == 10:
    #     breakpoint()

    position = monster.position
    direction = monster.direction
    x = position.x
    y = position.y
    vx = direction.x
    vy = direction.y

    r = BASE_RADIUS

    intercepts = []
    if vx == 0:
        p = Point(x, math.sqrt(r * r - x * x))
        if x >= -r and x <= r:
            intercepts = [Point(x, p), Point(x, -p)]
    else:
        a = vy / vx
        b = -1
        c = y - a * x + base.x

        x0 = -a * c / (a * a + b * b)
        y0 = -b * c / (a * a + b * b)

        if c * c < r * r * (a * a + b * b):
            d = r * r - c * c / (a * a + b * b)
            mult = math.sqrt(d / (a * a + b * b))

            intercepts = [
                p for p in [Point(x0 + b * mult, y0 - a * mult), Point(x0 - b * mult, y0 + a * mult)] if on_screen(p)
            ]

    if len(intercepts) > 0:
        monster.threat = True
        monster.distance_to_base = distance(base, position)


# base_x,base_y: The corner of the map representing your base
base_x, base_y = [int(i) for i in read_input().split()]
base = Point(base_x, base_y)
heroes_per_player = int(read_input())

# game loop
while True:
    my_health, my_mana = [int(j) for j in read_input().split()]
    if my_health < 0:
        break
    enemy_health, enemy_mana = [int(j) for j in read_input().split()]
    entity_count = int(read_input())  # Amount of heros and monsters you can see

    monsters = []
    my_heroes = []
    opp_heroes = []
    for i in range(entity_count):
        _id, _type, x, y, shield_life, is_controlled, health, vx, vy, near_base, threat_for = [
            int(j) for j in read_input().split()
        ]
        entity = Entity(
            _id,  # _id: Unique identifier
            _type,  # _type: 0=monster, 1=your hero, 2=opponent hero
            Point(x, y),  # x,y: Position of this entity
            shield_life,  # shield_life: Ignore for this league; Count down until shield spell fades
            is_controlled,  # is_controlled: Ignore for this league; Equals 1 when this entity is under a control spell
            health,  # health: Remaining health of this monster
            Point(vx, vy),  # vx,vy: Trajectory of this monster
            near_base,  # near_base: 0=monster with no target yet, 1=monster targeting a base
            threat_for,  # threat_for: Given this monster's trajectory, is it a threat to 1=your base, 2=your opponent's base, 0=neither
            False,
            0,
            None,
        )

        if _type == TYPE_MONSTER:
            monsters.append(entity)
        elif _type == TYPE_MY_HERO:
            my_heroes.append(entity)
        elif _type == TYPE_OP_HERO:
            opp_heroes.append(entity)

    for monster in monsters:
        intercept_with_base(monster)

    threat_monsters = [m for m in sorted(monsters, key=lambda m: m.distance_to_base) if m.threat]

    available_heroes = list(my_heroes)
    for monster in threat_monsters:
        print(f"{monster.id} {monster.threat} {monster.distance_to_base}", file=sys.stderr, flush=True)
        if available_heroes:
            sorted_heroes = sorted(available_heroes, key=lambda h: distance(h.position, monster.position))
            for h in sorted_heroes:
                print(f"HERO: {h.id} {distance(h.position, monster.position)}", file=sys.stderr, flush=True)

            hero = sorted_heroes[0]
            available_heroes.remove(hero)
            hero.monster_to_attack = monster

    for hero in my_heroes:
        monster = hero.monster_to_attack
        if monster:
            print(f"MOVE {monster.position.x} {monster.position.y}")
        else:
            print("WAIT")
