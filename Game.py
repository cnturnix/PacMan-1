from GameDefs import Pos
from GameDefs import SpriteType
from GameDefs import globals
from GameObject import GameObject
from Ghost import Ghost
from PacMan import PacMan
from Pill import Pill
import math
import heapq


def euclidean_heuristic(a, b):
    return math.sqrt((a.x - b.x) ** 2 + (a.y - b.y) ** 2)


def a_star_search(game, start, goal):
    frontier = []
    heapq.heappush(frontier, (0, start))
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0

    while frontier:
        current = heapq.heappop(frontier)[1]

        if current == goal:
            break

        for next in game.neighbors(current):
            if game.check_position(next):  # 检查是否是墙
                continue
            new_cost = cost_so_far[current] + euclidean_heuristic(current, next)
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + euclidean_heuristic(next, goal)
                heapq.heappush(frontier, (priority, next))
                came_from[next] = current

    # 重建路径
    path = []
    current = goal
    while current != start:
        path.append(current)
        current = came_from[current]
    path.reverse()
    return path


class Game:
    gameTime = 0
    addWalls = True

    def __init__(self):
        # Initialize game elements
        self.pacman = PacMan(Pos(15, 15))
        self.ghost = Ghost(Pos(1, 1))
        self.pill = Pill(Pos(15, 3))
        self.score = 0
        self.grid = [[None for x in range(globals.gameSize)] for y in range(globals.gameSize)]
        self.map = [[0 for x in range(globals.gameSize)] for y in range(globals.gameSize)]

        globals.pacman = self.pacman
        globals.ghost = self.ghost
        globals.pill = self.pill

        for i in range(globals.gameSize):
            self.map[i][0] = 1
            self.map[i][globals.gameSize - 1] = 1
            self.map[0][i] = 1
            self.map[globals.gameSize - 1][i] = 1
            GameObject(Pos(i, 0), SpriteType.WALL)
            GameObject(Pos(i, globals.gameSize - 1), SpriteType.WALL)
            GameObject(Pos(0, i), SpriteType.WALL)
            GameObject(Pos(globals.gameSize - 1, i), SpriteType.WALL)

        if Game.addWalls:

            for i in range(globals.gameSize // 2 - 3):
                self.map[i + globals.gameSize // 4 + 2][globals.gameSize // 4] = 1
                self.map[i + globals.gameSize // 4 + 2][globals.gameSize * 3 // 4] = 1
                self.map[globals.gameSize // 4][i + globals.gameSize // 4 + 2] = 1
                self.map[globals.gameSize * 3 // 4][i + globals.gameSize // 4 + 2] = 1

                GameObject(Pos(i + globals.gameSize // 4 + 2, globals.gameSize // 4), SpriteType.WALL)
                GameObject(Pos(i + globals.gameSize // 4 + 2, globals.gameSize * 3 // 4), SpriteType.WALL)

                GameObject(Pos(globals.gameSize // 4, i + globals.gameSize // 4 + 2), SpriteType.WALL)
                GameObject(Pos(globals.gameSize * 3 // 4, i + globals.gameSize // 4 + 2), SpriteType.WALL)

        for i in range(globals.gameSize):
            for j in range(globals.gameSize):
                if GameObject.checkCollisions(Pos(i, j)) == SpriteType.EMPTY:
                    self.grid[i][j] = GameObject(Pos(i, j), SpriteType.DOT)

        def check_position(self, pos):
            if 0 <= pos.x < len(self.map) and 0 <= pos.y < len(self.map[0]):
                return self.map[pos.x][pos.y] == 1  # 1 means wall
            return True  # Out of bounds is considered as wall

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



    def neighbors(self, pos):
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]  # 包括对角方向
        result = []
        for dx, dy in directions:
            neighbor = Pos(pos.x + dx, pos.y + dy)
            if 0 <= neighbor.x < globals.gameSize and 0 <= neighbor.y < globals.gameSize:
                result.append(neighbor)
        return result

    def check_position(self, pos):
        if 0 <= pos.x < globals.gameSize and 0 <= pos.y < globals.gameSize:
            return self.map[pos.x][pos.y] == 1  # 1 means wall
        return True  # Out of bounds is considered as wall

    # 增加使用 A* 算法的方法
    def handle_wall_collision(self, start, goal):
        path = a_star_search(self, start, goal)
        if path:
            # 可以根据生成的路径执行移动等操作
            return path

