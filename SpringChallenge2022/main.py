from dataclasses import dataclass
from dis import dis
import sys
from collections import namedtuple
import math
import functools
from tokenize import triple_quoted
from turtle import position

from inputs import input

TYPE_MONSTER = 0
TYPE_MY_HERO = 1
TYPE_OP_HERO = 2

MAX_WIDTH = 17630
MAX_HEIGHT = 9000
BASE_RADIUS = 5000
HERO_STEP = 800
MONSTER_STEP = 400
HEALTH_DECREASE = 2
BASE_SIZE = 300
WIND_RANGE = 1200
SPELL_RANGE = 2200

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
    monster_to_shield: "Entity"
    enemy_to_attack: "Entity"
    wind: bool
    shield: bool


def on_screen(p: Point):
    return p.x > 0 and p.x < MAX_WIDTH and p.y > 0 and p.y < MAX_HEIGHT


def distance(p1: Point, p2: Point):
    return math.sqrt((p2.x - p1.x) * (p2.x - p1.x) + (p2.y - p1.y) * (p2.y - p1.y))


def intercept_with_base(monster):
    # if monster.id == 6:
    #     breakpoint()

    position = monster.position
    direction = monster.direction
    x = position.x
    y = position.y
    vx = direction.x
    vy = direction.y

    r = BASE_RADIUS

    intercepts = False
    if vx == 0:
        intercepts = x >= base.x - r and x <= base.x + r
    else:
        a = vy / vx
        b = -1
        c = y - a * x
        dist = (abs(a * base.x + b * base.y + c)) / math.sqrt(a * a + b * b)
        intercepts = r >= dist

    if intercepts > 0:
        monster.threat = True
        monster.distance_to_base = distance(base, position)


# base_x,base_y: The corner of the map representing your base
base_x, base_y = [int(i) for i in read_input().split()]
base = Point(base_x, base_y)
first_base = base.x < MAX_WIDTH / 2
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
            None,
            None,
            False,
            False,
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

    available_heroes = [h for h in my_heroes if not h.is_controlled]
    enemies_near_base = [
        a for a in opp_heroes if not a.is_controlled and distance(a.position, base) < BASE_RADIUS + 1000
    ]
    monsters_near_hero = [
        m
        for m in threat_monsters
        if distance(m.position, base) < BASE_RADIUS and distance(m.position, hero.position) < WIND_RANGE
    ]
    print(
        "E near base",
        file=sys.stderr,
        flush=True,
    )
    print(
        [f"{m.id}" for m in enemies_near_base],
        file=sys.stderr,
        flush=True,
    )
    print(
        "M near E",
        file=sys.stderr,
        flush=True,
    )
    for monster in threat_monsters:
        if not available_heroes:
            break
        steps_to_base = math.ceil((monster.distance_to_base - BASE_SIZE) / MONSTER_STEP)
        strikes = steps_to_base * HEALTH_DECREASE
        heroes_needed = math.ceil(monster.health / strikes)
        print(
            f"{monster.id} {monster.distance_to_base} {monster.health} {heroes_needed}",
            file=sys.stderr,
            flush=True,
        )
        insuficient_heroes = heroes_needed > len(available_heroes)
        for i in range(heroes_needed):
            if available_heroes:
                sorted_heroes = sorted(available_heroes, key=lambda h: distance(h.position, monster.position))
                for h in sorted_heroes:
                    print(f"HERO: {h.id} {distance(h.position, monster.position)}", file=sys.stderr, flush=True)
                hero = sorted_heroes[0]
                available_heroes.remove(hero)
                enemies_near_hero = [e for e in enemies_near_base if distance(hero.position, e.position) < WIND_RANGE]
                hero.shield = len(enemies_near_hero) > 0
                if insuficient_heroes and distance(hero.position, monster.position) < WIND_RANGE or enemies_near_hero:
                    hero.wind = True
                elif len(monsters_near_hero) > 1:
                    hero.wind = True
                else:
                    hero.monster_to_attack = monster

    angle_step = math.pi / 2 / (heroes_per_player + 1)
    angles = [(a + 1) * angle_step for a in range(heroes_per_player)]
    s = 1 if first_base else -1
    available_bases = [
        Point(
            base.x + s * round((BASE_RADIUS + 1000) * math.cos(a)),
            base.y + s * round((BASE_RADIUS + 1000) * math.sin(a)),
        )
        for a in angles
    ]
    for hero in my_heroes:
        monster = hero.monster_to_attack
        monster_to_shield = hero.monster_to_shield
        enemy = hero.enemy_to_attack
        if monster:
            print(f"MOVE {monster.position.x} {monster.position.y}")
        elif hero.wind:
            print(f"SPELL WIND {round(MAX_WIDTH / 2)} {round(MAX_WIDTH / 2)}")
        elif monster_to_shield:
            if distance(hero.position, monster_to_shield.position) < SPELL_RANGE:
                print(f"SPELL SHIELD {monster_to_shield.id}")
            else:
                print(f"MOVE {monster_to_shield.position.x} {monster_to_shield.position.y}")
        elif enemy and distance(hero.position, enemy.position) < SPELL_RANGE:
            print(f"SPELL CONTROL {enemy.id} {round(MAX_WIDTH / 2)} {round(MAX_WIDTH / 2)}")
        elif enemy:
            print(f"MOVE {enemy.position.x} {enemy.position.y}")
        elif hero.shield and hero.shield_life <= 0:
            print(f"SPELL SHIELD {hero.id}")
        else:
            nearest_monster = None
            if distance(hero.position, base) > BASE_RADIUS:
                sorted_monsters = sorted(monsters, key=lambda m: distance(hero.position, m.position))
                if sorted_monsters:
                    nearest_monster = sorted_monsters[0]
                    d = distance(hero.position, nearest_monster.position)
                    if d < HERO_STEP * 5:
                        print(f"MOVE {nearest_monster.position.x} {nearest_monster.position.y}")
                    else:
                        nearest_monster = None
            if nearest_monster is None:
                nearest_base = sorted(available_bases, key=lambda b: distance(b, hero.position))[0]
                available_bases.remove(nearest_base)
                print(f"MOVE {nearest_base.x} {nearest_base.y}")
