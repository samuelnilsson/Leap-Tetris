import pygame
from abc import ABCMeta, abstractmethod
from random import randrange


def enum(**enums):
    return type('Enum', (), enums)


Color = enum(
    GREEN=1, RED=2, YELLOW=3, PINK=4, DARK_BLUE=5, LIGHT_BLUE=6, ORANGE=7)


class Block:

    def __init__(self, color):
        self.SIZE = 30
        self._color = color

    def get_image(self):
        if self._color == Color.GREEN:
            return pygame.image.load('assets/tetris_green.png')
        elif self._color == Color.RED:
            return pygame.image.load('assets/tetris_red.png')
        elif self._color == Color.YELLOW:
            return pygame.image.load('assets/tetris_yellow.png')
        elif self._color == Color.PINK:
            return pygame.image.load('assets/tetris_pink.png')
        elif self._color == Color.DARK_BLUE:
            return pygame.image.load('assets/tetris_dark_blue.png')
        elif self._color == Color.LIGHT_BLUE:
            return pygame.image.load('assets/tetris_light_blue.png')
        else:
            return pygame.image.load('assets/tetris_orange.png')


class Tetrimino:

    __metaclass__ = ABCMeta

    def __init__(self, grid, transparent):
        self.Rotation = enum(UP=1, RIGHT=2, DOWN=3, LEFT=4)
        self._rotation = self.Rotation.UP
        self._position = self._x, self._y = randrange(0, grid.WIDTH-3), 0 # -3: -2 for for "half tetrimino width" and -1 for zero indexed array.
        self.BRICK_SIZE = 30
        self._image = self.load_image()
        self._timer = 0
        self.GRID_WIDTH = grid.WIDTH
        self.GRID_HEIGHT = grid.HEIGHT
        self.SPEED = 50
        self._current_speed = 50
        self._transparent = transparent

    @abstractmethod
    def get_color(self):
        """returns the image to use for this tetrimino"""
        pass

    @abstractmethod
    def get_up_shape(self):
        """Returns a 5x5 list for when the brick is rotated upwards with
        zeros where there is no brick, ones where there is a brick and two
        where the rotation point is"""
        pass

    @abstractmethod
    def get_right_shape(self):
        """Returns a 5x5 list for when the brick is rotated to the right with
        zeros where there is no brick, ones where there is a brick and two
        where the rotation point is"""
        pass

    @abstractmethod
    def get_down_shape(self):
        """Returns a 5x5 list for when the brick is rotated downwards with
        zeros where there is no brick, ones where there is a brick and two
        where the rotation point is"""
        pass

    @abstractmethod
    def get_left_shape(self):
        """Returns a 5x5 list for when the brick is rotated to the left with
        zeros where there is no brick, ones where there is a brick and two
        where the rotation point is"""
        pass

    def set_transparent(self, transparent):
        self._transparent = transparent
        if not transparent:
            self._image = self.load_image()
        else:
            self._image = pygame.image.load('assets/transparent.png')

    def get_transparent(self):
        return self._transparent

    def get_current_shape(self):
        if self._rotation == self.Rotation.UP:
            return self.get_up_shape()
        if self._rotation == self.Rotation.RIGHT:
            return self.get_right_shape()
        if self._rotation == self.Rotation.DOWN:
            return self.get_down_shape()
        else:
            return self.get_left_shape()

    def on_loop(self):
        if (self._timer == self._current_speed):
            self._y += 1
            self._timer = 0
        self._timer += 1

    def on_event(self, event, grid, leap_mode):
        if not leap_mode:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.rotate_right(grid)
                if event.key == pygame.K_RIGHT:
                    self.move_right(grid)
                if event.key == pygame.K_LEFT:
                    self.move_left(grid)
                if event.key == pygame.K_DOWN:
                    self._timer = 5
                    self._current_speed = 5
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    self._current_speed = self.SPEED

    def rotate_right(self, grid):
        self._rotation = (self._rotation + 1) % 4
        if not self.is_inside_grid(grid):
            self._rotation = (self._rotation + 3) % 4

    def move_right(self, grid):
        self._x += 1
        if not self.is_inside_grid(grid):
            self._x -= 1

    def move_left(self, grid):
        self._x -= 1
        if not self.is_inside_grid(grid):
            self._x += 1

    def render_shape(self, shape, surface):
        """Renders the given shape on the given surface"""
        for x in range(0, 5):
            for y in range(0, 5):
                if shape[y][x] is not 0:
                    x_pos = self._x * self.BRICK_SIZE + x * self.BRICK_SIZE
                    y_pos = self._y * self.BRICK_SIZE + y * self.BRICK_SIZE
                    surface.blit(self._image, (x_pos, y_pos))

    def on_render(self, display_surface):
        if self._rotation == self.Rotation.UP:
            self.render_shape(self.get_up_shape(), display_surface)
        elif self._rotation == self.Rotation.RIGHT:
            self.render_shape(self.get_right_shape(), display_surface)
        elif self._rotation == self.Rotation.DOWN:
            self.render_shape(self.get_down_shape(), display_surface)
        else:
            self.render_shape(self.get_left_shape(), display_surface)

    def is_inside_grid(self, grid):
        """Returns true if the tetrimino is inside the grid"""
        for x in range(0, 5):
            for y in range(0, 5):
                if self.get_current_shape()[y][x] is not 0:
                    if (self._x + x) < 0 or (self._x + x) >= self.GRID_WIDTH:
                        return False
                    if grid[self._x + x][self._y + y] is not None:
                        return False
        return True

    def attach_current_tetrimino_to_grid(self, grid):
        for x in range(0, 5):
            for y in range(0, 5):
                if self.get_current_shape()[y][x] is not 0:
                    attach_x = self._x + x
                    attach_y = self._y + y
                    grid[attach_x][attach_y] = Block(
                        self.get_color())

    def is_termino_down(self, grid):
        """Returns true if the current tetrimino has landed on another
        tetrimino or on the floor."""
        y = 4
        while y >= 0:
            x = 4
            while x >= 0:
                tetrimino_x = self._x + x
                tetrimino_y = self._y + y
                if self.get_current_shape()[y][x] != 0:
                    if tetrimino_y is self.GRID_HEIGHT - 1:
                        return True
                    if grid[tetrimino_x][tetrimino_y + 1] is not None:
                        return True
                x = x - 1
            y = y - 1
        return False
