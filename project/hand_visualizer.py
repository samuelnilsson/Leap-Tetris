import pygame
import math


class Hand_visualizer:

    def __init__(self):
        self.RED = (0, 255, 0)
        self.LINE_WIDTH = 4
        self.LENGTH = 200

        self._color = self.RED
        self._line_position_x = 180
        self._line_position_y = 360
        self._start_position_x = 0
        self._start_position_y = 0
        self._end_position_x = 0
        self._end_position_y = 0
        self._hand_palm_normal_angle = math.pi

    def on_render(self, surface):
        pygame.draw.line(
            surface, self._color,
            (self._start_position_x, self._start_position_y),
            (self._end_position_x, self._end_position_y), 4)

    def on_loop(self):
        self.calculate_line()

    def calculate_line(self):
        """Calculates the lines start and en position from the angle of the
        normal of the hand palm"""
        line_angle = self._hand_palm_normal_angle - math.pi / 2
        self._start_position_y = math.sin(
            line_angle) * self.LENGTH / 2
        self._end_position_y = -self._start_position_y
        self._start_position_x = math.cos(
            line_angle) * self.LENGTH / 2
        self._end_position_x = -self._start_position_x

        self._start_position_y += self._line_position_y
        self._start_position_x += self._line_position_x
        self._end_position_y += self._line_position_y
        self._end_position_x += self._line_position_x
