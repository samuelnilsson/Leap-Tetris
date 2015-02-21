import pygame

from tetriminos import (i_tetrimino, j_tetrimino, l_tetrimino, o_tetrimino,
                        s_tetrimino, t_tetrimino, z_tetrimino)
import tetrimino


class Block:

    def __init__(self, color):
        self.SIZE = 30
        self._image = pygame
        self._color = color

    def get_image(self):
        if self._color == tetrimino.Color.GREEN:
            return pygame.image.load('assets/tetris_green.png')
        elif self._color == tetrimino.Color.RED:
            return pygame.image.load('assets/tetris_red.png')
        elif self._color == tetrimino.Color.YELLOW:
            return pygame.image.load('assets/tetris_yellow.png')
        elif self._color == tetrimino.Color.PINK:
            return pygame.image.load('assets/tetris_pink.png')
        elif self._color == tetrimino.Color.DARK_BLUE:
            return pygame.image.load('assets/tetris_dark_blue.png')
        elif self._color == tetrimino.Color.LIGHT_BLUE:
            return pygame.image.load('assets/tetris_red.png')
        else:
            return pygame.image.load('assets/tetris_orange.png')


class Grid:

    def __init__(self):
        self._grid_structure = self.init_grid_structure()
        self._current_tetrimino = l_tetrimino.L_tetrimino()

    def init_grid_structure(self):
        """Returns a grid structure without blocks"""
        grid = []
        for column in range(0, 11):
            col = []
            for row in range(0, 23):
                col.append(None)
            grid.append(col)
        grid[5][5] = Block(tetrimino.Color.GREEN)
        return grid

    def on_render(self, surface):
        for column in range(0, 11):
            for row in range(0, 23):
                if self._grid_structure[column][row] is not None:
                    x_pos = column * self._grid_structure[column][row].SIZE
                    y_pos = row * self._grid_structure[column][row].SIZE
                    surface.blit(self._grid_structure[column][row].get_image(),
                                 (x_pos, y_pos))
        self._current_tetrimino.on_render(surface)

    def on_loop(self):
        self._current_tetrimino.on_loop()

    def on_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self._current_tetrimino.rotate_right()
            if event.key == pygame.K_RIGHT:
                self._current_tetrimino.move_right()
            if event.key == pygame.K_LEFT:
                self._current_tetrimino.move_left()
