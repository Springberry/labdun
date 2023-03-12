class Entity:
    def __init__(self, x_position=0, y_position=0, symbol=''):
       self.x_position = x_position
       self.y_position = y_position
       self.symbol = symbol

    def set_position(self, new_x, new_y):
        self.x_position = new_x
        self.y_position = new_y
