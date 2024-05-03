from abc import abstractmethod

from GameDefs import SpriteType
from GameDefs import Direction
from GameDefs import Pos

from GameDefs import globals


class GameObject:
    gameObjects = []

    def __init__(self, p: Pos, t: SpriteType):
        self.startPos = p
        self.position = p
        self.type = t
        GameObject.gameObjects.append(self)

    @abstractmethod
    def move(self) -> Direction:
        return Direction.NONE

    def checkCollisions(self) -> SpriteType:
        """
        :self: GameObject | GameRefs.Pos
        :return: SpriteType

        对于传入的对象，检查是否有碰撞的对象

        如果是 Pos 对象，返回该位置的对象类型

        如果是 GameObject 对象，返回该对象位置的对象类型，如果是自己或者位置上没有对象则返回GameRefs.SpriteType.EMPTY
        """
        if isinstance(self, Pos):
            for go in GameObject.gameObjects:
                if go.position.x == self.x and go.position.y == self.y:
                    return go.type
        else:
            for go in GameObject.gameObjects:
                if go.position.x == self.position.x and go.position.y == self.position.y and go is not self:
                    return go.type
        return SpriteType.EMPTY

    def checkCollision(self, other) -> bool:
        """
        :self: GameObject
        :param other: GameObject
        :return: bool

        检查两个对象是否在同一个位置，如果是同一个对象则同样视为未发生碰撞
        """
        return self is not other and self.position.x == other.position.x and self.position.y == other.position.y

    def hide(self):
        """
        隐藏对象，将对象的位置设置为(-1, -1)
        """
        self.position = Pos(-1, -1)

    def reset(self):
        """
        重置对象的位置为初始位置
        """
        self.position = self.startPos

    def update(self):
        # Basic movement logic
        direction = self.move()

        if direction != Direction.NONE:
            newPos = Pos(self.position.x, self.position.y)
            if direction & Direction.LEFT:
                newPos.x -= 1
            if direction & Direction.RIGHT:
                newPos.x += 1
            if direction & Direction.UP:
                newPos.y -= 1
            if direction & Direction.DOWN:
                newPos.y += 1

            # Wrap around logic for the game boundaries
            newPos.x = (newPos.x + globals.gameSize) % globals.gameSize
            newPos.y = (newPos.y + globals.gameSize) % globals.gameSize

            # Check if the new position is not a wall before moving
            if globals.game.check_position(newPos) != SpriteType.WALL:
                self.position = newPos

    def __str__(self):
        """
        :self: GameObject
        :return: 该对象的类型和位置
        """
        return f'{self.type} at {self.position}'
