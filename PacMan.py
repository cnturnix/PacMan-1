from GameObject import GameObject
from GameDefs import SpriteType, Direction, globals, Pos
import random


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
    Direction_PacMan = {
        Direction.UP,
        Direction.DOWN,
        Direction.LEFT,
        Direction.RIGHT,
        Direction.UP | Direction.LEFT,
        Direction.UP | Direction.RIGHT,
        Direction.DOWN | Direction.LEFT,
        Direction.DOWN | Direction.RIGHT,
        Direction.NONE
    }
    def __init__(self, p):
        super().__init__(p, SpriteType.PACMAN)
        self.visited = set()
        self.behavior_tree = Selector(
            Condition(self.near_ghost),
            Condition(self.pill_active),
            Action(self.explore)
        )

    def move(self):
        self.behavior_tree.run()
        return self.direction

    def near_ghost(self):
        distance = abs(globals.ghost.position.x - self.position.x) + abs(globals.ghost.position.y - self.position.y)
        if distance < 10 and not globals.pill.isActive():
            self.direction = self.avoid_ghost()
            return True
        return False

    def pill_active(self):
        if globals.pill.isActive():
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
        self.direction = random.choice(directions)
        return True

    def avoid_ghost(self):
        best_direction = Direction.NONE
        max_distance = 0
        for d in PacMan.Direction_PacMan:
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
