
from GameObject import GameObject
from GameDefs import Pos

from GameDefs import SpriteType
from GameDefs import Direction
from GameDefs import globals


class PacMan(GameObject):
    def __init__(self, p):
        super().__init__(p, SpriteType.PACMAN)
        self.pill_time = 0

    def move(self):
        if False:
            # Try moving one to the right
            newPos = Pos(self.position.x+1, self.position.y)

        # check if there is a wall in the direction of the movement
            if globals.game.check_position(newPos) == SpriteType.WALL:
                return Direction.DOWN

        return Direction.RIGHT

    def eat(self, pill):
        pill.eaten()
        self.pill_time = 15

    def update(self):
        if self.pill_time > 0:
            self.pill_time -= 1
