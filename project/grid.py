from tetriminos import (i_tetrimino, j_tetrimino, l_tetrimino, o_tetrimino,
                        s_tetrimino, t_tetrimino, z_tetrimino)
from random import randint
import pygame
import hand_visualizer
import mode_switcher


class ScoreBoard:

    def __init__(self):
        self._points = 0
        pygame.font.init()
        self._font = pygame.font.SysFont('Arial', 36)
        self.POSITION = POSITION_X, POSITIONY = (270, 20)
        self._color = (255, 255, 255)

    def add_points_from_rows(self, number_of_removed_rows):
        self._points += 10*(number_of_removed_rows**2)

    def on_render(self, surface):
        text_surface = self._font.render(str(self._points), True, self._color)
        surface.blit(text_surface, self.POSITION)


class Grid:

    def __init__(self):
        self.HEIGHT = 24
        self.WIDTH = 12
        self._score_board = ScoreBoard()
        self._grid_structure = self.init_grid_structure()
        self._current_tetrimino = self.new_tetrimino()
        self._background_image = pygame.image.load('assets/background.png')
        self._hand_visualizer = hand_visualizer.Hand_visualizer()
        self._mode_switcher = mode_switcher.Mode_switcher()

    def init_grid_structure(self):
        """Returns a grid structure without blocks"""
        grid = []
        for column in range(0, self.WIDTH):
            col = []
            for row in range(0, self.HEIGHT):
                col.append(None)
            grid.append(col)
        return grid

    def on_render(self, surface):
        surface.blit(self._background_image, (0, 0))
        self._hand_visualizer.on_render(surface)
        for column in range(0, self.WIDTH):
            for row in range(0, self.HEIGHT):
                if self._grid_structure[column][row] is not None:
                    x_pos = column * self._grid_structure[column][row].SIZE
                    y_pos = row * self._grid_structure[column][row].SIZE
                    surface.blit(self._grid_structure[column][row].get_image(),
                                 (x_pos, y_pos))
        self._current_tetrimino.on_render(surface)
        self._score_board.on_render(surface)
        self._mode_switcher.on_render(surface)

    def on_loop(self):
        if self._current_tetrimino.is_termino_down(self._grid_structure):
            self._current_tetrimino.attach_current_tetrimino_to_grid(
                self._grid_structure)
            self._current_tetrimino = self.new_tetrimino()
            number_of_removed_rows = self.remove_full_rows()
            self._score_board.add_points_from_rows(number_of_removed_rows)
        else:
            self._current_tetrimino.on_loop()
        self._hand_visualizer.on_loop()

    def on_event(self, event):
        self._current_tetrimino.on_event(
            event, self._grid_structure, self._mode_switcher._leap_mode)
        self._mode_switcher.on_event(event)

    def new_tetrimino(self):
        """Returns a randomly generated tetrimino"""
        random_brick = randint(0, 6)
        if random_brick is 0:
            return i_tetrimino.I_tetrimino(self)
        if random_brick is 1:
            return j_tetrimino.J_tetrimino(self)
        if random_brick is 2:
            return l_tetrimino.L_tetrimino(self)
        if random_brick is 3:
            return o_tetrimino.O_tetrimino(self)
        if random_brick is 4:
            return s_tetrimino.S_tetrimino(self)
        if random_brick is 5:
            return t_tetrimino.T_tetrimino(self)
        if random_brick is 6:
            return z_tetrimino.Z_tetrimino(self)

    def remove_full_rows(self):
        number_of_removed_rows = 0
        for y in range(0, self.HEIGHT):
            row_full = True
            for x in range(0, self.WIDTH):
                if self._grid_structure[x][y] is None:
                    row_full = False
            if row_full:
                self.remove_row(y)
                number_of_removed_rows += 1
        return number_of_removed_rows

    def remove_row(self, row):
        for x in range(0, self.WIDTH):
            self._grid_structure[x][row] = None
        for tmp in range(0, row - 1):
            'It iterates from the bottom to the top'
            y = row - 1 - tmp
            for x in range(0, self.WIDTH):
                self._grid_structure[x][y + 1] = self._grid_structure[x][y]
                self._grid_structure[x][y] = None
