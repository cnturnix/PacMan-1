from GameDefs import Pos
from GameDefs import SpriteType
from GameDefs import globals
from GameObject import GameObject
from Ghost import Ghost
from PacMan import PacMan
from Pill import Pill
import heapq


class Node:
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position
        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position


class Game:
    gameTime = 0
    addWalls = True

    def __init__(self):
        # 初始化游戏元素
        self.pacman = PacMan(Pos(15, 15))
        self.ghost = Ghost(Pos(1, 1))
        self.pill = Pill(Pos(15, 3))
        self.score = 0
        self.grid = [[None for x in range(globals.gameSize)] for y in range(globals.gameSize)]
        self.map_for_astar = [[1 for x in range(globals.gameSize)] for y in range(globals.gameSize)]  # 1 表示可通过

        globals.pacman = self.pacman
        globals.ghost = self.ghost
        globals.pill = self.pill

        # 创建边界和内部墙壁
        for i in range(globals.gameSize):
            GameObject(Pos(i, 0), SpriteType.WALL)
            GameObject(Pos(i, globals.gameSize - 1), SpriteType.WALL)
            GameObject(Pos(0, i), SpriteType.WALL)
            GameObject(Pos(globals.gameSize - 1, i), SpriteType.WALL)

        if Game.addWalls:
            for i in range(globals.gameSize // 2 - 3):
                GameObject(Pos(i + globals.gameSize // 4 + 2, globals.gameSize // 4), SpriteType.WALL)
                GameObject(Pos(i + globals.gameSize // 4 + 2, globals.gameSize * 3 // 4), SpriteType.WALL)
                GameObject(Pos(globals.gameSize // 4, i + globals.gameSize // 4 + 2), SpriteType.WALL)
                GameObject(Pos(globals.gameSize * 3 // 4, i + globals.gameSize // 4 + 2), SpriteType.WALL)

        # 遍历整个地图，根据是否有游戏对象来更新map_for_astar
        for i in range(globals.gameSize):
            for j in range(globals.gameSize):
                if GameObject.checkCollisions(Pos(i, j)) != SpriteType.EMPTY:
                    self.map_for_astar[i][j] = 0  # 将有障碍物的位置设置为不可通行

        # 初始化地图中的点
        for i in range(globals.gameSize):
            for j in range(globals.gameSize):
                if GameObject.checkCollisions(Pos(i, j)) == SpriteType.EMPTY:
                    self.grid[i][j] = GameObject(Pos(i, j), SpriteType.DOT)

    def update(self):
        Game.gameTime += 1

        if self.grid[self.pacman.position.x][self.pacman.position.y] is not None:
            self.grid[self.pacman.position.x][self.pacman.position.y].hide()
            self.grid[self.pacman.position.x][self.pacman.position.y] = None
            self.score += 1

        # Update game elements
        self.pacman.update()
        self.ghost.update()
        self.pill.update()

        if self.pacman.checkCollision(self.pill):
            self.pacman.eat(self.pill)
        if self.pacman.checkCollision(self.ghost):
            if self.pacman.pill_time > 0:
                self.ghost.hide()
                self.score += 100
            else:
                # self.ghost.reset()
                print("Score: " + str(self.score))
                return True

        if Game.gameTime >= 1000:
            return True

        return False

    @staticmethod
    def check_position(p):
        for obj in GameObject.gameObjects:
            if obj.position.x == p.x and obj.position.y == p.y:
                return obj.type
        return SpriteType.EMPTY
