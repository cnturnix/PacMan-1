from time import sleep

from GameObject import GameObject
from GameDefs import Pos

from GameDefs import SpriteType
from GameDefs import Direction
from GameDefs import globals

import random

import keyboard


def check_key_pressed():
    keys = ['w', 'a', 's', 'd', 'space']
    # 检查并返回哪些键被按下
    return {key for key in keys if keyboard.is_pressed(key)}


# 行为树节点定义
class Node:
    def run(self):
        raise NotImplementedError


class Selector(Node):
    def __init__(self, *nodes):
        self.nodes = nodes

    def run(self):
        for node in self.nodes:
            if node.run():
                return True
        return False


class Condition(Node):
    def __init__(self, func):
        self.func = func

    def run(self):
        return self.func()


class Action(Node):
    def __init__(self, func):
        self.func = func

    def run(self):
        return self.func()


# 使用行为树管理 PacMan
class PacMan(GameObject):
    Direction_PacMan = [Direction.NONE,
                        Direction.UP, Direction.DOWN,
                        Direction.LEFT, Direction.RIGHT,
                        Direction.UP | Direction.LEFT, Direction.UP | Direction.RIGHT,
                        Direction.DOWN | Direction.LEFT, Direction.DOWN | Direction.RIGHT]

    def __init__(self, p):
        super().__init__(p, SpriteType.PACMAN)
        self.view_grid = [[None for _ in range(globals.gameSize)] for _ in range(globals.gameSize)]
        self.pill_time = 0
        self.visited = set()
        self.direction = Direction.NONE
        self.behavior_tree = Selector(

            Action(self.chase_ghost),
            Condition(self.near_ghost),
            Condition(self.pill_active),
            Action(self.explore)
        )

    def view(self):
        for i in range(globals.gameSize):
            for j in range(globals.gameSize):
                self.view_grid[i][j] = None
        for go in GameObject.gameObjects:
            if go.position.x == -1 and go.position.y == -1:
                continue
            self.view_grid[go.position.x][go.position.y] = go.type

    def move(self):
        self.view()
        while keyboard.is_pressed('ctrl'):
            sleep(0.5)
        # 检查键盘输入
        keys = check_key_pressed()
        if not keys:
            self.behavior_tree.run()
            return self.direction
        direction = Direction.NONE
        if 'space' in keys:
            return direction
        if 'w' in keys:
            direction |= Direction.UP
        if 's' in keys:
            direction |= Direction.DOWN
        if 'a' in keys:
            direction |= Direction.LEFT
        if 'd' in keys:
            direction |= Direction.RIGHT
        return direction

    def chase_ghost(self):
        if self.pill_time > 0:
            best_direction = Direction.NONE
            min_distance = float('inf')
            for d in self.Direction_PacMan:
                new_pos = self.calculate_new_position(d)
                if globals.game.check_position(new_pos) != SpriteType.WALL:
                    distance = abs(new_pos.x - globals.ghost.position.x) + abs(new_pos.y - globals.ghost.position.y)
                    if distance < min_distance:
                        min_distance = distance
                        best_direction = d
            self.direction = best_direction
            return True
        return False

    def near_ghost(self):
        distance = abs(globals.ghost.position.x - self.position.x) + abs(globals.ghost.position.y - self.position.y)
        if distance < 10 and distance < (abs(globals.pill.position.x - self.position.x) + abs(
                globals.pill.position.y - self.position.y)) and not self.pill_time > 0:
            self.direction = self.avoid_ghost()
            return True
        return False

    def pill_active(self):
        if not self.pill_time > 0:
            print("active")
            self.direction = self.move_towards(globals.pill.position)
            return True
        return False

    def explore(self):
        directions = list(Direction)
        random.shuffle(directions)
        for d in directions:
            new_pos = self.calculate_new_position(d)
            if new_pos not in self.visited and globals.game.check_position(new_pos) != SpriteType.WALL:
                self.visited.add(new_pos)
                self.direction = d
                return True
        return False  # 如果没有找到未访问的位置，则返回 False

    def avoid_ghost(self):
        best_direction = Direction.NONE
        max_distance = 0
        for d in Direction:
            new_pos = self.calculate_new_position(d)
            if globals.game.check_position(new_pos) != SpriteType.WALL:
                distance = abs(new_pos.x - globals.ghost.position.x) + abs(new_pos.y - globals.ghost.position.y)
                if distance > max_distance:
                    max_distance = distance
                    best_direction = d
        return best_direction

    def move_towards(self, target):
        best_direction = Direction.NONE
        min_distance = float('inf')
        for d in Direction:
            new_pos = self.calculate_new_position(d)
            if globals.game.check_position(new_pos) != SpriteType.WALL:
                distance = abs(new_pos.x - target.x) + abs(new_pos.y - target.y)
                if distance < min_distance:
                    min_distance = distance
                    best_direction = d
        return best_direction

    def calculate_new_position(self, direction):
        delta = {
            Direction.UP: (0, -1),
            Direction.DOWN: (0, 1),
            Direction.LEFT: (-1, 0),
            Direction.RIGHT: (1, 0),
            Direction.UP | Direction.LEFT: (-1, -1),
            Direction.UP | Direction.RIGHT: (1, -1),
            Direction.DOWN | Direction.LEFT: (-1, 1),
            Direction.DOWN | Direction.RIGHT: (1, 1),
            Direction.NONE: (0, 0)
        }
        dx, dy = delta[direction]
        return Pos(self.position.x + dx, self.position.y + dy)

    def eat(self, pill):
        pill.eaten()
        self.pill_time = 15

    def update(self):
        if self.pill_time > 0:
            self.pill_time -= 1
        super().update()
