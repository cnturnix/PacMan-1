from GameObject import GameObject
from GameDefs import SpriteType, Direction


class Pill(GameObject):
    def __init__(self, p):
        super().__init__(p, SpriteType.PILL)
        self.reset_time = 0

    def eaten(self):
        self.hide()
        self.reset_time = 30

    def update(self):
        if self.reset_time > 0:
            self.reset_time -= 1
        else:
            self.reset()

    def move(self):
        return Direction.NONE
