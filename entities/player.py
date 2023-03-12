from entities.entity import Entity

class Player(Entity):
    def __init__(self, x_position=0, y_position=0, symbol='@', health=10):
        super().__init__(x_position, y_position, symbol)
        self.health = health
