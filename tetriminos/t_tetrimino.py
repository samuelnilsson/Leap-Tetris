import tetrimino
import pygame


class T_tetrimino(tetrimino.Tetrimino):

    def get_color(self):
        return tetrimino.Color.RED

    def load_image(self):
        return pygame.image.load('assets/tetris_red.png')

    def get_up_shape(self):
        return [[0, 0, 0, 0, 0],
                [0, 0, 1, 0, 0],
                [0, 1, 2, 1, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0]]

    def get_right_shape(self):
        return [[0, 0, 0, 0, 0],
                [0, 0, 1, 0, 0],
                [0, 0, 2, 1, 0],
                [0, 0, 1, 0, 0],
                [0, 0, 0, 0, 0]]

    def get_down_shape(self):
        return [[0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 1, 2, 1, 0],
                [0, 0, 1, 0, 0],
                [0, 0, 0, 0, 0]]

    def get_left_shape(self):
        return [[0, 0, 0, 0, 0],
                [0, 0, 1, 0, 0],
                [0, 1, 2, 0, 0],
                [0, 0, 1, 0, 0],
                [0, 0, 0, 0, 0]]
