import tetrimino
import pygame


class S_tetrimino(tetrimino.Tetrimino):

    def get_color(self):
        return tetrimino.Color.PINK

    def load_image(self):
        return pygame.image.load('assets/tetris_pink.png')

    def get_up_shape(self):
        return [[0, 0, 0, 0, 0],
                [0, 0, 1, 1, 0],
                [0, 1, 2, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0]]

    def get_right_shape(self):
        return [[0, 0, 0, 0, 0],
                [0, 0, 1, 0, 0],
                [0, 0, 2, 1, 0],
                [0, 0, 0, 1, 0],
                [0, 0, 0, 0, 0]]

    def get_down_shape(self):
        return self.get_up_shape()

    def get_left_shape(self):
        return self.get_right_shape()
