import pygame
import math
from controls.controls import LeapControls
from controls.events import Events


class HandVisualizer:

    def __init__(self):
        self.GREEN = (0, 255, 0)
        self.YELLOW = (255, 255, 0)
        self.LINE_WIDTH = 4
        self.LENGTH = 200

        self._color = self.GREEN
        self._line_position_x = 180
        self._line_position_y = 360
        self._start_position_x = 0
        self._start_position_y = 0
        self._end_position_x = 0
        self._end_position_y = 0
        self._hand_palm_normal_angle = math.pi
        self._is_showed = False
        self._event_triggered = False

    def on_render(self, surface):
        if self._is_showed:
            if self._event_triggered:
                self._color = self.YELLOW
            else:
                self._color = self.GREEN
            pygame.draw.line(
                surface, self._color,
                (self._start_position_x, self._start_position_y),
                (self._end_position_x, self._end_position_y), 4)

    def on_loop(self, controls):
        if isinstance(controls, LeapControls):
            if controls._frame is not None:
                frame = controls._frame
                if frame.hands.is_empty:
                    self._is_showed = False
                    return
                else:
                    self._is_showed = True
                    hand = frame.hands[0]

                ymax = 330
                xmax = 200
                palm_direction = hand.palm_normal.normalized
                self._hand_palm_normal_angle = self.hand_angle(palm_direction)
                self._line_position_x = (hand.palm_position[0] + xmax) * 360 / (xmax * 2)
                self._line_position_y = -hand.palm_position[1] * 720 / ymax + 720
        else:
            self._is_showed = False
        self.calculate_line()

    def hand_angle(self, hand):
        return -math.atan2(hand[0], -hand[1])

    def calculate_line(self):
        """Calculates the lines start and en position from the angle of the
        normal of the hand palm"""
        line_angle = self._hand_palm_normal_angle
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
