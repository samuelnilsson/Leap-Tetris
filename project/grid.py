from tetriminos import (i_tetrimino, j_tetrimino, l_tetrimino, o_tetrimino,
                        s_tetrimino, t_tetrimino, z_tetrimino)
from random import randint
import copy
import pygame
import hand_visualizer
import mode_switcher
import controls.controls as controls


class ScoreBoard:

    def __init__(self):
        self._points = 0
        pygame.font.init()
        self._font = pygame.font.SysFont('Arial', 36)
        self.POSITION = POSITION_X, POSITIONY = (270, 20)
        self._color = (255, 255, 255)

    def add_points_from_rows(self, number_of_removed_rows):
        self._points += 10 * (number_of_removed_rows**2)

    def on_render(self, surface):
        text_surface = self._font.render(str(self._points), True, self._color)
        surface.blit(text_surface, self.POSITION)


class Grid:
    def __init__(self):
        self.HEIGHT              = 24
        self.WIDTH               = 12
        self._score_board        = ScoreBoard()
        self._grid_structure     = self.init_grid_structure()
        self._current_tetrimino  = self.new_tetrimino()
        self._shadowed_tetrimino = copy.deepcopy(self._current_tetrimino)
        self._background_image   = pygame.image.load('assets/background.png')
        self._hand_visualizer    = hand_visualizer.Hand_visualizer()
        self._paused             = False
        self._mode_switcher      = mode_switcher.Mode_switcher()
        self._controls           = controls.LeapControls()
        self._shadowed_tetrimino.set_transparent(True)


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

        self.render_where_to_land(surface)
        self._current_tetrimino.on_render(surface)
        self._score_board.on_render(surface)
        self._mode_switcher.on_render(surface)

        if self._paused:
            self.render_paused_text(surface)


    def render_paused_text(self, surface):
        fontsize = 70
        font = pygame.font.SysFont('Arial', fontsize)
        white = (255, 255, 255)
        text_surface = font.render('Paused', True, white)
        position = (60, 300)
        surface.blit(text_surface, position)


    def on_loop(self):
        if not self._paused:
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
        self._controls.on_event(event)

        if not self._paused:
            self._current_tetrimino.on_event(event, self._grid_structure)

        self._mode_switcher.on_event(event)


    def new_tetrimino(self):
        """Returns a randomly generated tetrimino"""
        random_brick = randint(0, 6)
        if random_brick is 0:
            return i_tetrimino.I_tetrimino(self, False)
        if random_brick is 1:
            return j_tetrimino.J_tetrimino(self, False)
        if random_brick is 2:
            return l_tetrimino.L_tetrimino(self, False)
        if random_brick is 3:
            return o_tetrimino.O_tetrimino(self, False)
        if random_brick is 4:
            return s_tetrimino.S_tetrimino(self, False)
        if random_brick is 5:
            return t_tetrimino.T_tetrimino(self, False)
        if random_brick is 6:
            return z_tetrimino.Z_tetrimino(self, False)


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


    def render_where_to_land(self, surface):
        """Renders a shadow showing where the terimino will land"""
        self._shadowed_tetrimino._position = self._current_tetrimino._position
        self._shadowed_tetrimino._x = self._current_tetrimino._x
        self._shadowed_tetrimino._y = self._current_tetrimino._y
        self._shadowed_tetrimino._rotation = self._current_tetrimino._rotation
        while not self._shadowed_tetrimino.is_termino_down(
                self._grid_structure):
            self._shadowed_tetrimino._y += 1
        self._shadowed_tetrimino.on_render(surface)
