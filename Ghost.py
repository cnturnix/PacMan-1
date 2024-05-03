import GameDefs
from GameObject import GameObject
from GameDefs import SpriteType
from GameDefs import Direction
from GameDefs import globals


class Ghost(GameObject):
    def __init__(self, p: GameDefs.Pos):
        super().__init__(p, SpriteType.GHOST)

    def move(self):
        direction = Direction.NONE
        if globals.pacman.position.y > self.position.y:
            direction |= Direction.DOWN
        if globals.pacman.position.y < self.position.y:
            direction |= Direction.UP
        if globals.pacman.position.x > self.position.x:
            direction |= Direction.RIGHT
        if globals.pacman.position.x < self.position.x:
            direction |= Direction.LEFT

        return direction
