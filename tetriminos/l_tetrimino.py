import tetrimino
import pygame


class L_tetrimino(tetrimino.Tetrimino):

    def get_color(self):
        return tetrimino.Color.LIGHT_BLUE

    def load_image(self):
        return pygame.image.load('assets/tetris_light_blue.png')

    def get_up_shape(self):
        return [[0, 0, 0, 0, 0],
                [0, 0, 0, 1, 0],
                [0, 1, 2, 1, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0]]

    def get_right_shape(self):
        return [[0, 0, 0, 0, 0],
                [0, 0, 1, 0, 0],
                [0, 0, 2, 0, 0],
                [0, 0, 1, 1, 0],
                [0, 0, 0, 0, 0]]

    def get_down_shape(self):
        return [[0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 1, 2, 1, 0],
                [0, 1, 0, 0, 0],
                [0, 0, 0, 0, 0]]

    def get_left_shape(self):
        return [[0, 0, 0, 0, 0],
                [0, 1, 1, 0, 0],
                [0, 0, 2, 0, 0],
                [0, 0, 1, 0, 0],
                [0, 0, 0, 0, 0]]
