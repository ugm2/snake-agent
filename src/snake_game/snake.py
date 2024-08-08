from .constants import GRID_SIZE, INITIAL_SNAKE_POSITION


class Snake:
    def __init__(self, grid_size=GRID_SIZE):
        self.grid_size = grid_size
        self.positions = [INITIAL_SNAKE_POSITION]
        self.direction = (1, 0)
        self.growing = False
        self.size = grid_size  # Snake occupies one full grid cell

    def set_direction(self, direction):
        if direction != (-self.direction[0], -self.direction[1]):
            self.direction = direction

    def move(self):
        head_x, head_y = self.positions[0]
        new_head = (head_x + self.direction[0] * self.grid_size, head_y + self.direction[1] * self.grid_size)
        self.positions.insert(0, new_head)
        if not self.growing:
            self.positions.pop()
        else:
            self.growing = False

    def grow(self):
        self.growing = True

    def has_collided_with_food(self, food_position, food_size):
        head_x, head_y = self.positions[0]
        food_x, food_y = food_position

        # Check if the food's top-left corner is within the snake's head area
        if (head_x <= food_x < head_x + self.size) and (head_y <= food_y < head_y + self.size):
            return True

        # TODO: Additional checks can be added for better precision, considering the actual size of the food
        return False

    def has_collided_with_wall(self, width, height):
        head_x, head_y = self.positions[0]
        return not (0 <= head_x < width and 0 <= head_y < height)

    def has_collided_with_self(self):
        return len(self.positions) != len(set(self.positions))