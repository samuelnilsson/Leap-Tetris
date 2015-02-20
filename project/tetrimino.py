import pygame
from abc import ABCMeta, abstractmethod


def enum(**enums):
    return type('Enum', (), enums)


class Tetrimino:

    __metaclass__ = ABCMeta

    def __init__(self):
        self._shape_right = self.get_right_shape()
        self._shape_left = self.get_left_shape()
        self._shape_up = self.get_up_shape()
        self._shape_down = self.get_down_shape()
        self._image_green = self.load_image()
        self.Rotation = enum(UP=1, RIGHT=2, DOWN=3, LEFT=4)
        self._rotation = self.Rotation.UP
        self._position = self._x, self._y = 0, 0
        self.BRICK_SIZE = 30
        self._timer = 0

    @abstractmethod
    def load_image(self):
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

    def on_loop(self):
        if (self._timer == 50):
            self._y += 1
            self._timer = 0
        self._timer += 1

    def rotate_right(self):
        self._rotation = (self._rotation + 1) % 4

    def move_right(self):
        self._x += 1

    def move_left(self):
        self._x -= 1

    def render_shape(self, shape, surface):
        """Renders the given shape on the given surface"""
        for x in range(0, 4):
            for y in range(0, 4):
                if shape[y][x] is not 0:
                    x_pos = self._x * self.BRICK_SIZE + x * self.BRICK_SIZE
                    y_pos = self._y * self.BRICK_SIZE + y * self.BRICK_SIZE
                    surface.blit(self._image_green, (x_pos, y_pos))

    def on_render(self, display_surface):
        if self._rotation == self.Rotation.UP:
            self.render_shape(self._shape_up, display_surface)
        elif self._rotation == self.Rotation.RIGHT:
            self.render_shape(self._shape_right, display_surface)
        elif self._rotation == self.Rotation.DOWN:
            self.render_shape(self._shape_down, display_surface)
        else:
            self.render_shape(self._shape_left, display_surface)
