import tetrimino
import pygame


class O_tetrimino(tetrimino.Tetrimino):

    def get_color(self):
        return tetrimino.Color.ORANGE

    def load_image(self):
        return pygame.image.load('assets/tetris_orange.png')

    def get_up_shape(self):
        return [[0, 0, 0, 0, 0],
                [0, 1, 1, 0, 0],
                [0, 1, 2, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0]]

    def get_right_shape(self):
        return self.get_up_shape()

    def get_down_shape(self):
        return self.get_up_shape()

    def get_left_shape(self):
        return self.get_up_shape()
