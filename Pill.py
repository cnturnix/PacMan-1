from GameObject import GameObject
from GameDefs import SpriteType, Direction
from GameDefs import Pos
from GameDefs import globals


class Pill(GameObject):
    def __init__(self, p):
        super().__init__(p, SpriteType.PILL)
        self.positions = 0
        self.reset_time = 0

    def eaten(self):
        self.hide()
        self.reset_time = 30

    def update(self):
        if self.reset_time > 0:
            self.reset_time -= 1
        elif self.position.x == -1 and self.position.y == -1:
            match self.positions:
                case 0:
                    self.position = Pos(self.startPos.x, globals.gameSize - self.startPos.y - 1)
                case 1:
                    self.position = Pos(globals.gameSize - self.startPos.y - 1, globals.gameSize - self.startPos.x - 1)
                case 2:
                    self.position = Pos(self.startPos.y, self.startPos.x)
                case _:
                    self.reset()

            self.positions = (self.positions + 1) % 4

    def move(self):
        return Direction.NONE
